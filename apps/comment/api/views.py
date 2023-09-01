from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from apps.post.models import Post
from apps.comment.models import Comment
from core.permissions import OwnerCommentOnly
from .serializers import CreateCommentSerializer,CommentSerializer

__all__ = [
    'PostCreateCommentAPIView',
    'PostListCommentsAPIView',
    'RepliesCommentAPIView',
    'DeleteCommentApiView',
]

class PostCreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comment'

    def post(self, request, pk_post):
        srz = self.serializer_class(data=request.data)

        if srz.is_valid():
            post = get_object_or_404(Post,pk=pk_post)
            srz_data = srz.data
            user = request.user
            text = srz_data['text']
            comment_id = srz_data.get('comment_id')
            if comment_id:
                if not Comment.objects.filter(post=post,id=comment_id).exists():
                    return Response({'comment_id':{'Comment with this id not exists.'}},status=status.HTTP_400_BAD_REQUEST)
                else:
                    replied_to = Comment.objects.get(post=post,id=comment_id)
            else:
                replied_to = None
            
            comment = Comment.objects.create(post=post,replied_to=replied_to,text=text,user=user)
            return Response(srz_data,status=status.HTTP_201_CREATED)
        else:
            return Response(srz.errors,status=status.HTTP_400_BAD_REQUEST)

class PostListCommentsAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('pk_post')
        return Comment.objects.filter(post_id=post_pk,replied_to=None)

class RepliesCommentAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_pk = self.kwargs.get('pk_comment')
        comment = get_object_or_404(Comment,pk=comment_pk)
        return Comment.objects.filter(replied_to=comment)

class DeleteCommentApiView(DestroyAPIView):
    permission_classes = [OwnerCommentOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'pk_comment'
