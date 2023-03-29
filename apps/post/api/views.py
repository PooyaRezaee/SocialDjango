from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from apps.post.models import Post
from .serializers import PostsSerializer,CreatePostSerializer,PostDetailSerializer
from core.permissions import IsOwnerOrReadOnly

__all__ = [
    'PostListsAPiView',
    'PostCreateApiView',
    'PostRUDApiView',
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
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'