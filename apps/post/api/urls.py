from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


app_name = 'post'

urlpatterns = [
    path('suggest/',PostListSuggestedAPIView.as_view(),name='suggest'),
    path('list/',PostsListAPiView.as_view(),name='list'),
    path('list/<str:username>/',PostUserListAPiView.as_view(),name='user-post'),
    path('create/',PostCreateApiView.as_view(),name='create'),
    path('<int:pk>/',PostRUDApiView.as_view(),name='post'),
    path('<int:pk>/like/', PostLikeAPIView.as_view()),
    path('<int:pk>/dislike/', PostDislikeAPIView.as_view()),
]