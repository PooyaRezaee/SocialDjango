from rest_framework import status
from rest_framework.test import APITestCase,APIClient,force_authenticate,APIRequestFactory
from django.urls import reverse
from apps.comment.models import Comment
from apps.comment.api.views import PostCreateCommentAPIView
from apps.post.models import Post
from apps.accounts.models import User

class PostCommentTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email="test@tt.tt", password='testpass')
        cls.post = Post.objects.create(title='Test post', text='Test content', author=cls.user)
        cls.factory = APIRequestFactory()

    def test_create_comment(self):
        view = PostCreateCommentAPIView.as_view()
        url = reverse('comment:create-comment', kwargs={'pk_post': self.post.pk})
        data = {'text': 'Test comment'}
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = view(request,pk_post=self.post.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_invalid_comment_id(self):
        view = PostCreateCommentAPIView.as_view()
        url = reverse('comment:create-comment', kwargs={'pk_post': self.post.pk})
        data = {'text': 'Test comment', 'comment_id': 100}
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = view(request, pk_post=self.post.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('comment_id', response.data)

    def test_list_comments(self):
        url = reverse('comment:post-list-comments', kwargs={'pk_post': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reply_comment(self):
        comment = Comment.objects.create(post=self.post, text='Test comment', user=self.user)
        url = reverse('comment:replys-comment', kwargs={'pk_comment': comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # TODO CHECK COMMENTS IN IT


