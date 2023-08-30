from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('suggest/', PostListSuggestedAPIView.as_view(), name='suggest'),
    path('list/', PostsListAPiView.as_view(), name='list'),
    path('list/<str:username>/', PostUserListAPiView.as_view(), name='user-post'),
    path('create/', PostCreateApiView.as_view(), name='create'),
    path('<int:pk>/', PostRUDApiView.as_view(), name='post'),
    path('like/', PostLikeAPIView.as_view(), name='like'),
    path('dislike/', PostDislikeAPIView.as_view(), name='dislike'),
]