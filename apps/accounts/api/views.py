from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.accounts.models import User
from django.db.models import Q,Count
from .serializers import ProfileImageSerializer,ProfileSerializer
from .mixins import ScopedRateThrottleForCUMixin


__all__ = [
    'TestAPI',
    'ProfilePictureAPIView',
    'SeeProfilePictureAPIView',
    'ProfileAPIView',
    'ProfileRetriveAPIView',
    'SearchUserApiView',
]


class TestAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer

    def get(self,request):
        return Response({'msg':f'Hello {request.user.username}'})


class ProfilePictureAPIView(ScopedRateThrottleForCUMixin,APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer
    throttle_scope = "profile"


    def get(self,request):
        srz = self.serializer_class(instance=request.user, context={'request': request})
        srz_data = srz.data
        return Response(srz_data)

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


class ProfileRetriveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'


class ProfileAPIView(ScopedRateThrottleForCUMixin,APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    throttle_scope = 'profile'

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


class SearchUserApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return Response({"detail": "Please provide a search query using the 'q' parameter in the URL."},
                            status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))

        count_matched = users.count()
        srz = self.serializer_class(users, many=True)

        return Response({'count': count_matched, 'users': srz.data})