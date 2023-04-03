from django.urls import path
from .views import *


app_name = 'comment'

urlpatterns = [
    path('create/<int:pk_post>/', PostCreateCommentAPIView.as_view(),name="create-comment"),
    path('list/<int:pk_post>/', PostListCommentsAPIView.as_view(),name='post-list-comments'),
    path('reply/<int:pk_comment>/', ReplysCommentAPIView.as_view(),name='replys-comment'),
    path('delete/<int:pk_comment>/', DeleteCommentApiView.as_view(),name='delete-comment'),
]