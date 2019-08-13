from rest_framework.permissions import IsAuthenticated

from apiv1.permissions import CanAddStaff
from .serializers import *
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)

        if s.is_valid():
            new_user_profile = s.save()
            response_data = UserProfileRetrieveSerializer(instance=new_user_profile).data

            return Response(response_data)
        else:
            return Response({'errors': s.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileRetrieveView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileRetrieveSerializer


class OrganizationCreateView(CreateAPIView):
    serializer_class = OrganizationCreateSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)

        if s.is_valid():
            new_organization = s.save()
            new_organization_data = OrganizationRetrieveSerializer(instance=new_organization).data
            return Response(new_organization_data)
        else:
            return Response({'errors': s.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationAddStaffView(CreateAPIView):
    serializer_class = StaffCreateSerializer
    permission_classes = [IsAuthenticated, CanAddStaff, ]

    def post(self, request, *args, **kwargs):
        organization = Organization.objects.get(pk=kwargs.get('organization_id'))
        s = self.serializer_class(data=request.data, context={'organization': organization})

        if s.is_valid():
            s = s.save()
            new_organization_data = OrganizationRetrieveSerializer(instance=s).data
            return Response(new_organization_data)
        else:
            return Response({'errors': s.errors}, status=status.HTTP_400_BAD_REQUEST)

