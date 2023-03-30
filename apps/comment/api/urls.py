from django.urls import path
from .views import *


app_name = 'comment'

urlpatterns = [
    path('create/<int:pk_post>/', PostCreateCommentAPIView.as_view()),
    path('list/<int:pk_post>/', PostListCommentsAPIView.as_view()),
    path('reply/<int:pk_comment>/', ReplysCommentAPIView.as_view()),
]