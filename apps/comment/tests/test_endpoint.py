from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from apps.comment.models import Comment
from apps.post.models import Post
from apps.accounts.models import User

class PostCommentTests(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email="test@tt.tt", password='testpass')
        self.post = Post.objects.create(title='Test post', text='Test content', author=self.user)

        # Get Jwt Token
        login_data = {'username': 'testuser', 'password': 'testpass'}
        url_data = reverse('account:token_obtain_pair')
        token_response = self.client.post(url_data, data=login_data)
        self.token = token_response.json()['access']

    def test_create_comment(self):
        url = reverse('comment:create-comment', kwargs={'pk_post': self.post.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'text': 'Test comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_invalid_comment_id(self):
        url = reverse('comment:create-comment', kwargs={'pk_post': self.post.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'text': 'Test comment', 'comment_id': 100}
        response = self.client.post(url, data)
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


