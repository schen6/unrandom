
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from django.http.response import JsonResponse
# from django.http import Http404
import sys

from rest_framework.response import Response
from rest_framework.decorators import api_view
from kol.models import Profile, Post #Brand, Attribute, Product , KolBasicData,
from kol.serializers import ProfileSerializer, AutocompleteProfileSerializer, PostSerializer #BrandSerializer, AttributeSerializer, ProductSerializer #, KolBasicDataSerializer,
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connection
from core.decorators import standardize_api_response
# Create your views here.
from .services import get_group_post_analytics, translate
import json


@api_view(['POST'])
def get_translate(request):
    try:

        text_to_translate = request.data.get('text', '')
        translated_text = translate(text_to_translate)  # Function from your Python script
        return Response({'text_en': translated_text})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def group_post_analytics_view(request):
    group_id = request.query_params.get('group_id', None)
    aggregation = request.query_params.get('aggregation', 'Day')
    range_days = request.query_params.get('range', 90)

    if group_id is not None:
        try:
            group_id = int(group_id)  # Convert to integer
            range_days = int(range_days)  # Convert range to integer

            analytics = get_group_post_analytics(group_id, aggregation, range_days)
            return JsonResponse(analytics, safe=False)

        except ValueError as e:
            # Handle value errors for group_id and range_days
            return HttpResponseBadRequest(f"Invalid parameter: {e}")

        except Exception as e:
            # Handle other exceptions, possibly log them
            return HttpResponseBadRequest(str(e))

    return HttpResponseBadRequest("group_id parameter is required")


@api_view(['GET'])
# @standardize_api_response
def ProfileApi(request):
    paginator = PageNumberPagination()
    query = request.query_params.get('query', None)
    paginator.page_size = request.query_params.get('size', 25)
    id = request.query_params.get('uid', 0)
    sort = request.query_params.get('sort', '')
    # paginator.page_size = 25  # Adjust the page size here

    if request.method == 'GET':
        # Fetch query parameter
        if id:
            try:
                profile = Profile.objects.get(pk=id)
                profile_serializer = ProfileSerializer(profile)
                return Response(profile_serializer.data)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if query:
            profiles = Profile.objects.filter(username__icontains=query)
        else:
            profiles = Profile.objects.all()

        # Apply sorting
        sort_fields = sort.split(',') if sort else []
        if len(sort_fields) == 2:
            sort_field, sort_order = sort_fields
            sort_field = '-' + sort_field if sort_order == 'desc' else sort_field
            profiles = profiles.order_by(sort_field)

        # Apply pagination
        result_page = paginator.paginate_queryset(profiles, request)
        profile_serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(profile_serializer.data)


@api_view(['GET'])
# @standardize_api_response
def autocomplete_search(request):
    query = request.query_params.get('query', '')
    if query:
        # First, try to find usernames that start with the query and sort by follower count
        profiles = Profile.objects.filter(username__istartswith=query).order_by('-followers')[:5]

        # If there are less than 5 results, supplement with 'contains' search
        if profiles.count() < 5:
            additional_profiles = Profile.objects.filter(username__icontains=query).exclude(uid__in=profiles).order_by('-followers')[:5 - profiles.count()]
            profiles = list(profiles) + list(additional_profiles)

        serializer = AutocompleteProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    return Response([])


@api_view(['GET'])
def PostApi(request):
    paginator = PageNumberPagination()
    query = request.query_params.get('query', '')
    post_id = request.query_params.get('id', None)
    uid = request.query_params.get('uid', None)
    paginator.page_size = request.query_params.get('size', 25)

    if query:
        # Full-text search across multiple columns
        raw_sql = """
                SELECT * FROM kol_post 
                WHERE title &@ %s OR summary &@ %s OR content &@ %s OR ocr_content &@ %s OR vid_to_text &@ %s;
            """
        with connection.cursor() as cursor:
            cursor.execute(raw_sql, [query, query, query, query, query])
            columns = [col[0] for col in cursor.description]
            rows = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        # Handle pagination
        page = paginator.paginate_queryset(rows, request)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

    elif post_id:
        # Fetch a specific post by ID
        try:
            post = Post.objects.get(pk=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Fetch all posts by a specific user
    try:
        posts = Post.objects.filter(uid=uid)
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Fallback if pagination is not applicable
    serializer = PostSerializer(rows, many=True)
    return Response(serializer.data)

# @csrf_exempt
# def generic_tag_api(request, tag_model, tag_serializer, id_field_name, tag_id=0):
#     if request.method == 'GET':
#         # Same logic as your previous code, just replacing 'brand' with 'tag'
#         page_number = request.GET.get('page', 1)
#         items_per_page = request.GET.get('items_per_page', 20)
#         sort_column = request.GET.get('sort_column')
#         sort_direction = request.GET.get('sort_direction')
#
#         all_tags = tag_model.objects.all()
#
#         if sort_column is not None and sort_direction is not None:
#             if sort_direction == 'desc':
#                 sort_column = '-' + sort_column
#             all_tags = all_tags.order_by(sort_column)
#
#         paginator = Paginator(all_tags, items_per_page)
#         tags = paginator.get_page(page_number)
#         tag_serializer_instance = tag_serializer(tags, many=True)
#
#         return JsonResponse({
#             'tags': tag_serializer_instance.data,
#             'total_pages': paginator.num_pages,
#             'current_page': page_number,
#         }, safe=False)
#
#     elif request.method == 'POST':
#         tag_data = JSONParser().parse(request)
#         tag_serializer_instance = tag_serializer(data=tag_data)
#         if tag_serializer_instance.is_valid():
#             tag_serializer_instance.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#
#     elif request.method == 'PUT':
#         tag_data = JSONParser().parse(request)
#         # Use id_field_name instead of the hardcoded 'id'
#         lookup = {id_field_name: tag_data[id_field_name]}
#         tag = tag_model.objects.get(**lookup)
#         tag_serializer_instance = tag_serializer(tag, data=tag_data)
#         if tag_serializer_instance.is_valid():
#             tag_serializer_instance.save()
#             return JsonResponse("Updated Successfully", safe=False)
#         return JsonResponse("Failed to Update", safe=False)
#
#     elif request.method == 'DELETE':
#         # Use id_field_name instead of the hardcoded 'id'
#         lookup = {id_field_name: tag_id}
#         tag = tag_model.objects.get(**lookup)
#         tag.delete()
#         return JsonResponse("Deleted Successfully", safe=False)


# Now you can create views for each tag type by calling the generic view with the appropriate model and serializer:

# @csrf_exempt
# def brand_api(request, id=0):
#     return generic_tag_api(request, Brand, BrandSerializer, 'brand_id', id)
#
#
# @csrf_exempt
# def product_api(request, id=0):
#     return generic_tag_api(request, Product, ProductSerializer, 'prod_id', id)
#
# @csrf_exempt
# def attribute_api(request, id=0):
#     return generic_tag_api(request, Attribute, AttributeSerializer, 'attribute_id', id)

#
# @csrf_exempt
# def BrandApi(request, id=0):
#     if request.method == 'GET':
#         # Get the 'page' parameter from the request, default to 1
#         page_number = request.GET.get('page', 1)
#
#         # Get the 'items_per_page' parameter from the request, default to 25
#         items_per_page = request.GET.get('items_per_page', 20)
#
#         # Get the sort parameters from the request
#         sort_column = request.GET.get('sort_column')
#         sort_direction = request.GET.get('sort_direction')
#
#         # Get all brands
#         all_brands = Brand.objects.all()
#
#         # Sort the brands
#         if sort_column is not None and sort_direction is not None:
#             if sort_direction == 'desc':
#                 sort_column = '-' + sort_column
#             all_brands = all_brands.order_by(sort_column)
#
#         # Create a Paginator object
#         paginator = Paginator(all_brands, items_per_page)
#
#         # Get the brands for the requested page
#         brands = paginator.get_page(page_number)
#
#         # Serialize the brands
#         brand_serializer = BrandSerializer(brands, many=True)
#
#         # Return the serialized brands
#         return JsonResponse({
#             'brands': brand_serializer.data,
#             'total_pages': paginator.num_pages,
#             'current_page': page_number,
#         }, safe=False)
#
#     elif request.method == 'POST':
#         brand_data = JSONParser().parse(request)
#         brand_serializer = BrandSerializer(data=brand_data)
#         if brand_serializer.is_valid():
#             brand_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#
#     elif request.method == 'PUT':
#         brand_data = JSONParser().parse(request)
#         brand = Brand.objects.get(brand_id=brand_data['brand_id'])  # use brand_id instead of id
#         brand_serializer = BrandSerializer(brand, data=brand_data)
#         if brand_serializer.is_valid():
#             brand_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#
#     elif request.method == 'DELETE':
#         brand = Brand.objects.get(brand_id=id)  # use brand_id instead of id
#         brand.delete()
#         return JsonResponse("Deleted Successfully",safe=False)


# @csrf_exempt
# def SaveFile(request):
#     file = request.FILES['file']
#     file_name = default_storage.save(file.name, file)
#     return JsonResponse(file_name, safe=False)



#
# @csrf_exempt
# def KolApi(request, id=0):
#     if request.method == 'GET':
#         kols = Kol.objects.all()
#         kol_serializer = KolSerializer(kols, many=True)
#         return JsonResponse(kol_serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         kol_data = JSONParser().parse(request)
#         # kol_data.pop('id', None)  # Remove 'id' from the data
#         kol_serializer = KolSerializer(data=kol_data)
#         if kol_serializer.is_valid():
#             kol_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#
#     elif request.method == 'PUT':
#         kol_data = JSONParser().parse(request)
#         kol = Kol.objects.get(id=kol_data['id'])
#         kol_serializer = KolSerializer(kol, data=kol_data)
#         if kol_serializer.is_valid():
#             kol_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#
#     elif request.method == 'DELETE':
#         kol = Kol.objects.get(id=id)
#         kol.delete()
#         return JsonResponse("Deleted Successfully",safe=False)
#
#
# @csrf_exempt
# def KolBasicDataApi(request, id=0):
#     if request.method == 'GET':
#         kolbasicdata = KolBasicData.objects.all()
#         kolbasicdata_serializer = KolBasicDataSerializer(kolbasicdata, many=True)
#         return JsonResponse(kolbasicdata_serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         kolbasicdata = JSONParser().parse(request)
#         kolbasicdata_serializer = KolBasicDataSerializer(data=kolbasicdata)
#         if kolbasicdata_serializer.is_valid():
#             kolbasicdata_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#
#     elif request.method == 'PUT':
#         kolbasicdata = JSONParser().parse(request)
#         kol = KolBasicData.objects.get(id=kolbasicdata['id'])
#         kolbasicdata_serializer = KolBasicDataSerializer(kol, data=kolbasicdata)
#         if kolbasicdata_serializer.is_valid():
#             kolbasicdata_serializer.save()
#             return JsonResponse("Updated Successfully", safe=False)
#         return JsonResponse("Failed to Update")
#
#     elif request.method == 'DELETE':
#         kolbasicdata = KolBasicData.objects.get(id=id)
#         kolbasicdata.delete()
#         return JsonResponse("Deleted Successfully", safe=False)