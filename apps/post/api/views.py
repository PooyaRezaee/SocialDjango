from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status
from apps.post.models import Post,Like
from .serializers import PostsSerializer,CreatePostSerializer,PostDetailSerializer
from core.permissions import IsOwnerOrReadOnly

__all__ = [
    'PostListsAPiView',
    'PostCreateApiView',
    'PostRUDApiView',
    'PostLikeAPIView',
    'PostDislikeAPIView',
]

class PostListsAPiView(ListAPIView):
    serializer_class = PostsSerializer
    queryset = Post.public_posts.all()

class PostCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        author = self.request.user

        serializer.save(author=author)

class PostRUDApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'

class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        if Like.objects.filter(post=post,user=user).exists():
            return Response({'msg':'You have already liked'},status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.create(post=post,user=user)
        return Response({'status':'ok'},status=status.HTTP_200_OK)

class PostDislikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        if not Like.objects.filter(post=post,user=user).exists():
            return Response({'msg':'You have not liked'},status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.filter(post=post,user=user)
        like.delete()
        return Response({'status':'ok'},status=status.HTTP_200_OK)