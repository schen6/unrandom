from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group, GroupKOLAssociation
from kol.models import Profile
from .serializers import GroupSerializer, GroupKOLAssociationSerializer
from core.decorators import standardize_api_response
from django.db import IntegrityError


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @standardize_api_response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupKOLAssociationViewSet(viewsets.ModelViewSet):
    queryset = GroupKOLAssociation.objects.all()
    serializer_class = GroupKOLAssociationSerializer
    permission_classes = [IsAuthenticated]

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

