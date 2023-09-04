from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from django.shortcuts import get_object_or_404
from apps.accounts.models import User
from apps.connection.models import Follow
from .serializers import FollowUsersSerializer
from .mixins import PrivetAccountRequired
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

__all__ = [
    'FollowUserAPIView',
    'UnFollowUserAPIView',
    'FollowersListAPIView',
    'FollowingsListAPIView',
    'FollowersInRequestAPIView',
    'AcceptRequestFollowAPIView',
    'RemoveFollowerApiView',
    'RejectRequestFollowAPIView',
]

class FollowUserAPIView(APIView):
    """
    Follow a User
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'follow'

    def post(self,request):
        username_target_user = request.data['username']
        resualt = request.user.follow(username_target_user)
        if resualt[0]:
            return Response({'msg': resualt[1]}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': resualt[1]}, status=status.HTTP_400_BAD_REQUEST)


class UnFollowUserAPIView(APIView):
    """
    UnFollow a User
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'unfollow'

    def post(self,request):
        username_target_user = request.data['username']
        resualt = request.user.unfollow(username_target_user)

        if resualt[0]:
            return Response({'msg': resualt[1]},status=status.HTTP_200_OK)
        else:
            return Response({'detail': resualt[1]},status=status.HTTP_400_BAD_REQUEST)

class FollowersListAPIView(APIView):
    """
    Get List FOllowers a user
    """

    permission_classes = [IsAuthenticated]
    serializer_Class = FollowUsersSerializer

    @method_decorator(cache_page(60))
    def get(self,request,username):
        target_user = get_object_or_404(User,username=username)
        user = request.user

        if (target_user != user) and (target_user.private_account and (not user in target_user.followers_real)):
            return Response({'detail': "You Don't have accesss"},status=status.HTTP_403_FORBIDDEN)

        followers_objs = target_user.followers_real

        srz = self.serializer_Class(instance=followers_objs, many=True, context={'request': request})

        return Response(srz.data, status=status.HTTP_200_OK)

class FollowingsListAPIView(APIView):
    """
    Get list followings a user
    """

    permission_classes = [IsAuthenticated]
    serializer_Class = FollowUsersSerializer

    @method_decorator(cache_page(60))
    def get(self,request,username):
        target_user = get_object_or_404(User, username=username)
        user = request.user

        if (target_user != user) and (target_user.private_account and (not user in target_user.followers_real)):
            return Response({'detail': "You Don't have accesss"},status=status.HTTP_403_FORBIDDEN)

        followings_objs = target_user.followings_real

        srz = self.serializer_Class(instance=followings_objs, many=True, context={'request': request})

        return Response(srz.data,status=status.HTTP_200_OK)


class FollowersInRequestAPIView(ListAPIView,PrivetAccountRequired):
    """
    Get List of request follow for user authonticated
    this endpoint is just for privet accouts
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FollowUsersSerializer

    def get_queryset(self):
        user = self.request.user
        return user.followers_in_reqest


class AcceptRequestFollowAPIView(APIView,PrivetAccountRequired):
    """
    Accept request follow a user
    """

    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        username_target_user = request.data['username']

        request_query = user.followers_in_reqest.filter(username=username_target_user)
        if request_query.exists():
            request_obj = request_query.get()

            try:
                follow_obj = Follow.objects.get(following=request_obj, follower=user)
                follow_obj.in_request = False
                follow_obj.save()

                return Response({'msg': f'accept request follow {request_obj.username}'})
            except IntegrityError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            msg_problem = "don't have follow request with this username"
            return Response({"detail": msg_problem},status=status.HTTP_400_BAD_REQUEST)


class RejectRequestFollowAPIView(APIView):
    """
    Reject request follow a user
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        username_target_user = request.data['username']

        request_query = user.followers_in_reqest.filter(username=username_target_user)
        if request_query.exists():
            request_obj = request_query.get()

            try:
                follow_obj = Follow.objects.get(following=request_obj, follower=user, in_request=True)
                follow_obj.delete()

                return Response({'msg': f'Rejected request follow {username_target_user}'})
            except IntegrityError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            msg_problem = "don't have follow request with this username"
            return Response({"detail": msg_problem}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFollowerApiView(APIView):
    """
    Remove a user from followers user authonticated
    """

    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        username_target_user = request.data['username']

        try:
            user_following = User.objects.get(username=username_target_user)
        except ObjectDoesNotExist:
            return Response({"detail": "User with this username does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Follow.objects.get(following=user_following, follower=user, in_request=False).delete()
            return Response({"msg": f"removed {username_target_user} from your followers"})
        except ObjectDoesNotExist:
            return Response({"detail": "User don't follow you."}, status=status.HTTP_400_BAD_REQUEST)

