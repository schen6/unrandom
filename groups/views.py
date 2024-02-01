from django.db import transaction
from django.db.models import F, OuterRef, Subquery
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group, GroupKOLAssociation
from kol.models import Profile, Post
from .serializers import GroupSerializer, GroupKOLAssociationSerializer, KolAssociationSerializer
from kol.serializers import PostUserSerializer
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import QueryDict
import json
from datetime import datetime, timedelta


@api_view(['GET'])
def GetGroupPostDetail(request):
    '''
    returns all posts for a particular group.  accepts time range.
    '''
    user = request.user
    paginator = PageNumberPagination()
    paginator.page_size = request.query_params.get('size', 25)
    group_id = request.query_params.get('group_id', None)

    try:
        days = int(request.query_params.get('range', 90))
    except ValueError:
        return Response({"error": "Invalid range parameter"}, status=400)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    if not group_id:
        return Response({"error": "group_id parameter is required"}, status=400)

    queryset = GroupKOLAssociation.objects.filter(group__user=user, group_id=group_id)
    uids = queryset.values_list('uid', flat=True)

    # Fetch posts within the time range for these UIDs
    queryset = Post.objects.filter(uid__in=uids, created_at_timestamp__range=[start_date, end_date])

    result_page = paginator.paginate_queryset(queryset, request)
    serializer = PostUserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetGroupDetail(request):
    '''
    return full list of uids for a specific group
    '''
    user = request.user
    paginator = PageNumberPagination()
    paginator.page_size = request.query_params.get('size', 25)
    group_id = request.query_params.get('group_id', None)
    query = request.query_params.get('query', None)
    sort = request.query_params.get('sort', None)

    # Start with a queryset of GroupKOLAssociation
    queryset = GroupKOLAssociation.objects.filter(group__user=user)

    if group_id:
        queryset = queryset.filter(group_id=group_id)

    if query:
        # Filter based on Profile username in GroupKOLAssociation
        queryset = queryset.filter(uid__username__icontains=query)

    # Apply sorting
    # sort_fields = sort.split(',') if sort else []
    # if len(sort_fields) == 2:
    #     sort_field, sort_order = sort_fields
    #     sort_field = '-' + sort_field if sort_order == 'desc' else sort_field
    #     queryset = queryset.order_by(sort_field)

    if sort:
        sort_field, sort_order = sort.split(',') if ',' in sort else (sort, 'asc')
        sort_annotate = f'sort_{sort_field}'
        queryset = queryset.annotate(**{sort_annotate: F(f'uid__{sort_field}')})
        if sort_order == 'desc':
            queryset = queryset.order_by(f'-{sort_annotate}')
        else:
            queryset = queryset.order_by(sort_annotate)

    # Apply pagination
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = KolAssociationSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    '''
    manage groups belonging to a user.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.request.query_params.get('group_id')
        # Return groups for the current user only
        if group_id:
            return Group.objects.filter(id=group_id,user=self.request.user).prefetch_related('group_associations')
        else:
            return Group.objects.filter(user=self.request.user).prefetch_related('group_associations')

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        instance.group_name = f"group_{instance.id}"
        instance.save()


class GroupKOLAssociationViewSet(viewsets.ModelViewSet):
    '''
    used to add / delete kols from a specific group belonging to a user.
    '''
    queryset = GroupKOLAssociation.objects.all()
    serializer_class = GroupKOLAssociationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        uids = request.data.get('uid', [])  # List of uids

        if not group_id or not uids:
            return Response(
                {"detail": "Missing group_id or uids"},
                status=status.HTTP_400_BAD_REQUEST
            )

        associations = []
        for uid in uids:
            try:
                profile = Profile.objects.get(uid=uid)
                association, created = GroupKOLAssociation.objects.get_or_create(
                    group_id=group_id,
                    uid=profile,
                    defaults={'group_id': group_id, 'uid': profile}
                )
                if created:
                    associations.append(association)
            except Profile.DoesNotExist:
                return Response(
                    {"detail": f"Profile with uid {uid} does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(associations, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):

        group_id = request.data.get('group_id')
        uids = request.data.get('uid', [])  # List of uids

        if not group_id or not uids:
            return Response(
                {"detail": "Missing group_id or uids"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch associations to be deleted
        associations = GroupKOLAssociation.objects.filter(
            group_id=group_id, uid__in=uids
        )

        # Check if all uids exist in the group
        if associations.count() != len(uids):
            return Response(
                {"detail": "Some uids are not associated with the group"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform deletion
        associations.delete()

        return Response(
            {"detail": "Associations successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

# def perform_create(self, serializer):
#     # Get the KOL UID from the request
#     kol_uid = self.request.data.get('profile')
#
#     # Check if the KOL UID exists in the Profile model
#     if not Profile.objects.filter(uid=kol_uid).exists():
#         return Response(
#             {"error": "KOL with the provided UID does not exist."},
#             status=status.HTTP_400_BAD_BAD_REQUEST
#         )
#
#     # If the UID exists, save the association
#     serializer.save()




# user = request.user
# paginator = PageNumberPagination()
# query = request.query_params.get('query', None)
# paginator.page_size = request.query_params.get('size', 25)
# group_id = request.query_params.get('group_id', '')
# sort = request.query_params.get('sort', '')
# # paginator.page_size = 25  # Adjust the page size here
# # Fetch query parameter
# if group_id:
#
#     queryset = Group.objects.filter(id=group_id, user=user).prefetch_related('group_associations')
#     if query:
#         # Adjust this line to match your actual model relationships
#         queryset = queryset.filter(group_associations__uid__username__icontains=query)
#
#     # Apply sorting
#     sort_fields = sort.split(',') if sort else []
#     if len(sort_fields) == 2:
#         sort_field, sort_order = sort_fields
#         sort_field = '-' + sort_field if sort_order == 'desc' else sort_field
#         queryset = queryset.order_by(sort_field)
#
#     if not queryset.exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     # serializer = GroupDetailSerializer(queryset, many=True)
#
#     # Apply pagination
#     result_page = paginator.paginate_queryset(queryset, request)
#     serializer = GroupDetailSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)
#
#     # return Response(serializer.data)

#
# class GroupDetailViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupDetailSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # Return groups for the current user only
#         group_id = self.request.query_params.get('group_id')
#         if group_id:
#             return Group.objects.filter(id=group_id, user=self.request.user).prefetch_related('group_associations')
#         else:
#             return Group.objects.filter(user=self.request.user).prefetch_related('group_associations')

