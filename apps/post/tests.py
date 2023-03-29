from django.test import TestCase
from apps.accounts.models import User
from .models import Post,Comment,Like


class PostModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.tags = ['test1','test2','test3']
        cls.user = User.objects.create_user(username='testuser',email="test@t.tt", password='testpass')
        cls.post = Post.objects.create(title='Test Post', text='Test content', author=cls.user,tags=cls.tags)

    def test_post_str(self):
        self.assertEquals(str(self.post), 'Test Post')

    def test_tags_posts(self):
        for tag in self.tags:
            self.assertTrue(tag in self.post.tags)


class LikeModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser',email="test@t.tt", password='testpass')
        cls.post = Post.objects.create(title='Test Post', text='Test content', author=cls.user)
        cls.like = Like.objects.create(user=cls.user, post=cls.post)


    def test_like_str(self):
        self.assertEquals(str(self.like), str(self.user))

    def test_like_post(self):
        self.assertEqual(self.post.likes.count(), 1)

    def test_dislike_post(self):
        self.like.delete()
        self.assertEqual(self.post.likes.count(), 0)




class CommentModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser',email="test@t.tt", password='testpass')
        cls.post = Post.objects.create(title='Test Post', text='Test content', author=cls.user)
        cls.comment = Comment.objects.create(post=cls.post, text='Test comment', user=cls.user)

    def test_comment_str(self):
        self.assertEquals(str(self.comment), str(self.user))

    def test_comment_for_post(self):
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first(), self.comment)

    def test_reply_to_comment(self):
        comment_rep = Comment.objects.create(post=self.post, text='Test reply', user=self.user,replied_to=self.comment)

        self.assertEqual(self.comment.reply.count(), 1)
        self.assertEqual(self.comment.reply.first(), comment_rep)
