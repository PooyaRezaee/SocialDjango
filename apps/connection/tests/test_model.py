from django.test import TestCase
from apps.connection.models import Follow
from model_bakery import baker
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

class ModelFollowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = baker.make('accounts.User')
        cls.user2 = baker.make('accounts.User')
        cls.user3 = baker.make('accounts.User')

        # user1 => user2,user3
        Follow.objects.create(following=cls.user1,follower=cls.user2,in_request=False)
        Follow.objects.create(following=cls.user1,follower=cls.user3,in_request=False)

        # user2 => user1
        Follow.objects.create(following=cls.user2,follower=cls.user1,in_request=False)

        # user3 ==in-request=> user2
        Follow.objects.create(following=cls.user3,follower=cls.user2,in_request=True)

    def test_count_followers(self):
        self.assertEqual(self.user1.followers_real.count(),1)
        self.assertEqual(self.user2.followers_real.count(),1)
        self.assertEqual(self.user3.followers_real.count(),1)

    def test_count_following(self):
        self.assertEqual(self.user1.followings_real.count(),2)
        self.assertEqual(self.user2.followings_real.count(),1)
        self.assertEqual(self.user3.followings_real.count(),0)

    def test_count_followers_in_request(self):
        self.assertEqual(self.user1.followers_in_reqest.count(), 0)
        self.assertEqual(self.user2.followers_in_reqest.count(), 1)
        self.assertEqual(self.user3.followers_in_reqest.count(), 0)

    def test_count_following_in_request(self):
        self.assertEqual(self.user1.followings_in_reuest.count(), 0)
        self.assertEqual(self.user2.followings_in_reuest.count(), 0)
        self.assertEqual(self.user3.followings_in_reuest.count(), 1)

    def test_follow_with_method_follow_user(self):
        user = baker.make('accounts.User')
        self.assertTrue(user.follow(self.user1.username))
        self.assertEqual(user.followers_real.count(),0)
        self.assertEqual(user.followings_real.count(),1)

    def test_duplicated_follow(self):
        user1 = baker.make('accounts.User')
        user2 = baker.make('accounts.User')
        Follow.objects.create(following=user1, follower=user2, in_request=False)
        with self.assertRaises(IntegrityError):
            Follow.objects.create(following=user1, follower=user2, in_request=False)
        self.assertEqual(user2.followers.count(), 1)

    def test_follow_self(self):
        user1 = baker.make('accounts.User')
        with self.assertRaises(ValidationError):
            Follow.objects.create(following=user1, follower=user1, in_request=False)
        self.assertEqual(user1.followers.count(), 0)

