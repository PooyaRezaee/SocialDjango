from django.urls import path
from .views import *


app_name = 'connection'

urlpatterns = [
    path('follow/', FollowUserAPIView.as_view(),name="follow"),
    path('unfollow/', UnFollowUserAPIView.as_view(),name="unfollow"),
    path('followers/<str:username>/', FollowersListAPIView.as_view(),name="followers"),
    path('followings/<str:username>/', FollowingsListAPIView.as_view(),name="followings"),
    path('requests/', FollowersInRequestAPIView.as_view(),name="request-followers"),
    path('request-accept/', AcceptRequestFollowAPIView.as_view(),name="accept-request-followers"),
    path('request-reject/', RejectRequestFollowAPIView.as_view(),name="reject-request-followers"),
    path('remove-follower/', RemoveFollowerApiView.as_view(),name="remove-followers"),
]