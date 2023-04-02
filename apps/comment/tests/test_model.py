from django.test import TestCase
from apps.comment.models import Comment
from apps.post.models import Post
from apps.accounts.models import User



class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email="test@t.tt", password='testpass')
        cls.post = Post.objects.create(title='Test Post', text='Test content', author=cls.user)
        cls.comment = Comment.objects.create(post=cls.post, text='Test comment', user=cls.user)

    def test_comment_str(self):
        self.assertEquals(str(self.comment), str(self.user))

    def test_comment_for_post(self):
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first(), self.comment)

    def test_reply_to_comment(self):
        comment_rep = Comment.objects.create(post=self.post, text='Test reply', user=self.user, replied_to=self.comment)

        self.assertEqual(self.comment.reply.count(), 1)
        self.assertEqual(self.comment.reply.first(), comment_rep)