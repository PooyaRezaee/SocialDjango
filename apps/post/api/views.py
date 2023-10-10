from django.db.models import Q,Count,F
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status

from core.permissions import IsOwnerOrReadOnly
from apps.post.models import Post,Like
from .serializers import PostsSerializer,CreatePostSerializer,PostDetailSerializer
from .mixins import ForPrivetPageFollowingRequired

__all__ = [
    'PostsListAPiView',
    'PostCreateApiView',
    'PostRUDApiView',
    'PostLikeAPIView',
    'PostDislikeAPIView',
    'PostListSuggestedAPIView',
    'PostUserListAPiView',
    'SearchPostApiView',
    'PostListTrendingAPIView',
]


class PostListSuggestedAPIView(APIView):
    """
    Get List Suggest posts
    """

    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        following_usernames = [user.username for user in user.followings_real]
        follower_usernams = [user.username for user in user.followers_real]

        suggested_posts = Post.objects.filter(Q(author__username__in=following_usernames) | Q(author__username__in=follower_usernams))

        suggested_posts = suggested_posts.order_by('-created')
        serializer = PostsSerializer(suggested_posts, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class PostListTrendingAPIView(APIView):
    """
    Get List Trending posts
    """

    permission_classes = [AllowAny]

    def get(self,request):
        datetime_now = timezone.now()
        delta_recent_time_for_like = timezone.timedelta(hours=48)
        delta_recent_time_for_post = timezone.timedelta(days=120)

        start_datetime_for_post = datetime_now - delta_recent_time_for_post
        start_datetime_for_like = datetime_now - delta_recent_time_for_like

        posts = Post.objects.filter(created__range=(start_datetime_for_post,datetime_now))
        # Add Weight by "follower X1 , like X10 , view X5"

        count_recent_likes = Count('likes', filter=Q(likes__liked_at__range=(start_datetime_for_like,datetime_now)))
        count_author_followers = Count('author__followers')
        # count_views = Count() TODO Add after initlize system view counter

        posts = posts.annotate(count_recent_likes=count_recent_likes,count_author_followers=count_author_followers)
        posts = posts.annotate(Weight=((F('count_recent_likes') * 10) + (F('count_author_followers') * 1)))

        trending_posts = posts.order_by('-Weight')
        serializer = PostsSerializer(trending_posts, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class PostUserListAPiView(ForPrivetPageFollowingRequired, ListAPIView):
    """
    Get list of posts a user
    if page user is private must you have follow that
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer

    def get_queryset(self,*args,**kwargs):
        username = self.kwargs.get('username')
        return Post.objects.filter(author__username=username)


class PostsListAPiView(ListAPIView):
    """
    List all of posts public
    """

    permission_classes = [AllowAny]
    serializer_class = PostsSerializer
    queryset = Post.public_posts.all()

    # method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PostCreateApiView(CreateAPIView):
    """
    Create New post
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'post'

    def perform_create(self, serializer):
        author = self.request.user

        serializer.save(author=author)


class PostRUDApiView(RetrieveUpdateDestroyAPIView):
    """
    Read Post for each have access
    Update Delete post by owner it
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'


class PostLikeAPIView(APIView):
    """
    Like a post
    """

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
    """
    Dislike a post
    """

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
    """
    Search by send query string 'q' for title and text & 'tag' for tag a post
    You can use two filter together
    """

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

