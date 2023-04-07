from django.urls import path
from .views import *


app_name = 'connection'

urlpatterns = [
    path('follow/', FollowUserAPIView.as_view(),name="follow"),
    path('unfollow/', UnFollowUserAPIView.as_view(),name="unfollow"),
    path('followers/<str:username>/', FollowersListAPIView.as_view(),name="followers"),
    path('followings/<str:username>/', FollowingsListAPIView.as_view(),name="followings"),
]