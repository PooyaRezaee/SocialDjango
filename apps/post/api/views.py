from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status
from apps.post.models import Post,Like
from .serializers import PostsSerializer,CreatePostSerializer,PostDetailSerializer
from .mixins import ForPrivetPageFollowingRequired
from core.permissions import IsOwnerOrReadOnly
from django.db.models import Q,Count
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# from django.views.decorators.vary import vary_on_cookie, vary_on_headers

__all__ = [
    'PostsListAPiView',
    'PostCreateApiView',
    'PostRUDApiView',
    'PostLikeAPIView',
    'PostDislikeAPIView',
    'PostListSuggestedAPIView',
    'PostUserListAPiView',
    'SearchPostApiView',
]


class PostListSuggestedAPIView(APIView):
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

    # method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PostCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'post'

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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'like'

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


class SearchPostApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PostsSerializer
    queryset = Post.public_posts.all()

    def get(self, request):
        q = request.GET.get('q')
        tag = request.GET.get('tag')
        if not(q or tag):
            return Response({"detail": "Please provide a search query using the 'q' or 'tag' parameter in the URL."},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset

        if tag:
            quertset = queryset.filter(tags__name=tag)

        if q:
            # matching_posts = Post.objects.filter(Q(title__icontains=q) | Q(text__icontains=q)) # NOTE SIMPLE
            queryset = queryset.annotate(
                num_matches=Count('title', filter=Q(title__icontains=q)) + Count('text', filter=Q(text__icontains=q))
            ).filter(
                Q(title__icontains=q) | Q(text__icontains=q)
            ).order_by('-num_matches')

        count_matched = queryset.count()
        srz = self.serializer_class(queryset,many=True)

        return Response({'count': count_matched, 'posts': srz.data})

