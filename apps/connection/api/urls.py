from django.urls import path
from .views import *


app_name = 'connection'

urlpatterns = [
    path('follow/', FollowUserAPIView.as_view(),name="follow"),
    path('unfollow/', UnFollowUserAPIView.as_view(),name="unfollow"),
]