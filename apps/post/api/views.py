from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework import status
from apps.post.models import Post,Like
from .serializers import PostsSerializer,CreatePostSerializer,PostDetailSerializer
from .mixins import ForPrivetPageFollowingRequired
from core.permissions import IsOwnerOrReadOnly
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

__all__ = [
    'PostsListAPiView',
    'PostCreateApiView',
    'PostRUDApiView',
    'PostLikeAPIView',
    'PostDislikeAPIView',
    'PostListSuggestedAPIView',
    'PostUserListAPiView',
]


class PostListSuggestedAPIView(APIView): # TODO MUST SET CACHED
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        following_usernames = [user.username for user in user.followings_real]
        follower_usernams = [user.username for user in user.followers_real]

        suggested_posts = Post.objects.filter(Q(author__username__in=following_usernames) | Q(author__username__in=follower_usernams))

        suggested_posts = suggested_posts.order_by('-created')
        serializer = PostsSerializer(suggested_posts, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class PostUserListAPiView(ForPrivetPageFollowingRequired, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer

    def get_queryset(self,*args,**kwargs):
        username = self.kwargs.get('username')
        return Post.objects.filter(author__username=username)


class PostsListAPiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostsSerializer
    queryset = Post.public_posts.all()


class PostCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        author = self.request.user

        serializer.save(author=author)


class PostRUDApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'


class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        pk = data.get('pk')
        if not pk:
            return Response({"detail":"You must send pk filed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"detail": f"Post with pk {pk} doe's not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if Like.objects.filter(post=post,user=user).exists():
            return Response({'detail': 'You have already liked'}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(post=post,user=user)
        return Response({'msg': f'post {pk} liked'}, status=status.HTTP_200_OK)


class PostDislikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        pk = data.get('pk')
        if not pk:
            return Response({"detail": "You must send pk filed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"detail": f"Post with pk {pk} doe's not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        like_obj = Like.objects.filter(post=post, user=user)
        if like_obj.exists():
            like_obj.delete()
            return Response({'msg': f'Post {pk} disliked'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': "You Don't have like on this post"}, status=status.HTTP_400_BAD_REQUEST)

