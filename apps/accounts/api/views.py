from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.accounts.models import User
from .serializers import ProfileImageSerializer,ProfileSerializer


__all__ = [
    'TestAPI',
    'ChangeProfilePictureAPIView',
    'SeeProfilePictureAPIView',
    'ProfileAPIView',
]

class TestAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer

    def get(self,request):
        return Response({'status':'OK'})

class ChangeProfilePictureAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer


    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.profile_picture:
                user.profile_picture.delete()
            user.profile_picture = serializer.validated_data['profile_picture']
            user.save()
            return Response({'status': 'ok'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user = request.user
        if user.profile_picture:
            user.profile_picture.delete()
            user.profile_picture = None
            user.save()
            return Response({'detail': "Profile picture deleted successfully."},status=status.HTTP_200_OK)
        else:
            return Response({'detail': "No profile picture found to delete."},status=status.HTTP_400_BAD_REQUEST)


class SeeProfilePictureAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileImageSerializer
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(self.get_queryset(), username=self.kwargs['username'])

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self,request):
        user = request.user
        srz = self.serializer_class(instance=user)
        return Response(srz.data,status=status.HTTP_200_OK)

    def patch(self,request):
        user = request.user
        srz = self.serializer_class(instance=user,data=request.data,partial=True)
        if srz.is_valid():
            srz.save()
            return Response(srz.data,status=status.HTTP_200_OK)
        else:
            return Response(srz.errors,status=status.HTTP_400_BAD_REQUEST)