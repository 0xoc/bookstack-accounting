from .serializers import UserProfileCreateSerializer, UserProfileRetrieveSerializer
from rest_framework.generics import CreateAPIView
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

