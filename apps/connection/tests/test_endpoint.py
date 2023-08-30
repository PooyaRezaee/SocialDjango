from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from model_bakery import baker
from apps.connection.models import Follow

class EndPointFollowTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.user1 = baker.make('accounts.User')
        cls.user2 = baker.make('accounts.User')

        cls.user3_privet = baker.make('accounts.User',private_account=True)
        cls.user4_privet = baker.make('accounts.User',private_account=True)

    def test_follow_user(self):
        self.client.force_authenticate(user=self.user1)
        data = {'username':self.user2.username}
        response = self.client.post(reverse('connection:follow'), data=data)
        self.assertEqual(response.status_code,200)
        self.assertTrue(Follow.objects.filter(following=self.user1,follower=self.user2).exists())

    def test_unfollow_user(self):
        self.user1.follow(self.user2)
        self.client.force_authenticate(user=self.user1)
        data = {'username': self.user2.username}
        response = self.client.post(reverse('connection:unfollow'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Follow.objects.filter(following=self.user1, follower=self.user2).exists())

    def test_follow_and_unfollow_user_with_invalid_username(self):
        self.client.force_authenticate(user=self.user1)
        data = {'username': 'temp'}
        response1 = self.client.post(reverse('connection:follow'), data=data)
        response2 = self.client.post(reverse('connection:unfollow'), data=data)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_duplicate_follow_user(self):
        self.user1.follow(self.user2)
        self.client.force_authenticate(user=self.user1)
        data = {'username': self.user2.username}
        response = self.client.post(reverse('connection:follow'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_unfollow_user_no_follow(self):
        self.client.force_authenticate(user=self.user1)
        data = {'username': self.user2.username}
        response = self.client.post(reverse('connection:unfollow'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_see_followers_and_followings_privet_account_without_access(self):
        Follow.objects.create(following=self.user3_privet,follower=self.user4_privet,in_request=False)

        self.client.force_authenticate(user=self.user4_privet)
        response_followers = self.client.get(reverse('connection:followers',kwargs={'username':self.user3_privet.username}))
        response_followings = self.client.get(reverse('connection:followings',kwargs={'username':self.user3_privet.username}))
        self.assertEqual(response_followers.status_code,403)
        self.assertEqual(response_followings.status_code,403)

    def test_see_followers_and_followings_privet_account_with_access(self):
        Follow.objects.create(following=self.user3_privet,follower=self.user4_privet,in_request=False)

        self.client.force_authenticate(user=self.user3_privet)
        response_followers = self.client.get(reverse('connection:followers',kwargs={'username':self.user4_privet.username}))
        response_followings = self.client.get(reverse('connection:followings',kwargs={'username':self.user4_privet.username}))
        self.assertEqual(response_followers.status_code,200)
        self.assertEqual(response_followings.status_code,200)


    def test_see_followers_and_followings_privet_account_with_self(self):
        Follow.objects.create(following=self.user3_privet, follower=self.user4_privet,in_request=False)

        self.client.force_authenticate(user=self.user3_privet)
        response_followers = self.client.get(reverse('connection:followers', kwargs={'username': self.user4_privet.username}))
        response_followings = self.client.get(reverse('connection:followings', kwargs={'username': self.user4_privet.username}))
        self.assertEqual(response_followers.status_code, 200)
        self.assertEqual(response_followings.status_code, 200)