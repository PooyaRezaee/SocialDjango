from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

__all__ = [
    'FollowUserAPIView',
    'UnFollowUserAPIView',
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
