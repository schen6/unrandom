
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from django.http.response import JsonResponse
# from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from kol.models import Profile #Brand, Attribute, Product , KolBasicData,
from kol.serializers import ProfileSerializer, AutocompleteProfileSerializer #BrandSerializer, AttributeSerializer, ProductSerializer #, KolBasicDataSerializer,
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from core.decorators import standardize_api_response
# Create your views here.


@api_view(['GET'])
@standardize_api_response
def ProfileApi(request, id=0):
    paginator = PageNumberPagination()
    paginator.page_size = 10  # You can adjust the page size here

    if request.method == 'GET':
        # Search functionality
        username = request.query_params.get('username', None)
        if username:
            profiles = Profile.objects.filter(username__icontains=username)
        elif id == 0:
            profiles = Profile.objects.all()
        else:
            try:
                profile = Profile.objects.get(pk=id)
                profile_serializer = ProfileSerializer(profile)
                return Response(profile_serializer.data)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        # Pagination is applied here
        result_page = paginator.paginate_queryset(profiles, request)
        profile_serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(profile_serializer.data)


@api_view(['GET'])
@standardize_api_response
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