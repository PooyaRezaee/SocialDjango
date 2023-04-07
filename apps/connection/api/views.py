from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.accounts.models import User
from .serializers import FollowUsersSerializer

__all__ = [
    'FollowUserAPIView',
    'UnFollowUserAPIView',
    'FollowersListAPIView',
    'FollowingsListAPIView',
]

class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,requests):
        username_target_user = requests.data['username']
        if requests.user.follow(username_target_user):
            return Response({'status': 'ok'},status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User Followed or Not Found'},status=status.HTTP_404_NOT_FOUND)


class UnFollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,requests):
        username_target_user = requests.data['username']
        if requests.user.unfollow(username_target_user):
            return Response({'status': 'ok'},status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User Not follow you or not found'},status=status.HTTP_404_NOT_FOUND)

class FollowersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_Class = FollowUsersSerializer

    def get(self,request,username):
        target_user = get_object_or_404(User,username=username)
        user = request.user

        if (target_user != user) and (target_user.private_account and (not user in target_user.followers_real)):
            return Response({'detail':'You Must Be Follwer this user'},status=status.HTTP_403_FORBIDDEN)

        followers_objs = target_user.followers_real

        srz = self.serializer_Class(instance=followers_objs, many=True)

        return Response(srz.data, status=status.HTTP_200_OK)

class FollowingsListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_Class = FollowUsersSerializer

    def get(self,request,username):
        target_user = get_object_or_404(User, username=username)
        user = request.user

        if (target_user != user) and (target_user.private_account and (not user in target_user.followers_real)):
            return Response({'detail':'You Must Be Follwer this user'},status=status.HTTP_403_FORBIDDEN)

        followings_objs = target_user.followings_real

        srz = self.serializer_Class(instance=followings_objs,many=True)

        return Response(srz.data,status=status.HTTP_200_OK)
