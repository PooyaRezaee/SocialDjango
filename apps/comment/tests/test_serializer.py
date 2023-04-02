from rest_framework.test import APITestCase,APIClient
from apps.comment.api.serializers import CreateCommentSerializer, CommentSerializer
from apps.comment.models import Comment
from apps.post.models import Post
from apps.accounts.models import User

class SerializerCommentTests(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email="test@tt.tt", password='testpass')
        self.post = Post.objects.create(title='Test post', text='Test content', author=self.user)


    def test_comment_serializer(self):
        user = User.objects.create_user(username='testuser2',email='testuser2@t.tt', password='testpass')
        comment = Comment.objects.create(post=self.post, text='Test comment', user=user)
        serializer = CommentSerializer(instance=comment)
        expected_data = {
            'id': comment.id,
            'text': comment.text,
            'user': user.username,
            'created': serializer.get_humanize_time(str(comment.created)),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_create_comment_serializer(self):
        comment = Comment.objects.create(post=self.post, text="It's Great", user=self.user)
        data = {'text': 'Test comment', 'comment_id': comment.id}
        serializer = CreateCommentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['text'], 'Test comment')
        self.assertEqual(serializer.validated_data['comment_id'], comment.id)