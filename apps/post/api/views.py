from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post
from .serializers import PostsSerializer,CreatePostSerializer


__all__ = [
    'PostListsAPiView',
    'PostCreateApiView',
]

class PostListsAPiView(ListAPIView):
    serializer_class = PostsSerializer
    queryset = Post.objects.all()

class PostCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        author = self.request.user

        serializer.save(author=author)


class PostRUDApiView(RetrieveUpdateDestroyAPIView):
    pass