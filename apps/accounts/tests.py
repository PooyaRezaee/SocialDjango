from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from apps.accounts.models import User

class EndPointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(username='testuser', email="test@tt.tt", password='testpass')

        cls.login_data = {'username':'testuser', 'password':'testpass'}
        cls.url_test = reverse('account:test-iauth')
        cls.url_token = reverse('account:token_obtain_pair')
        cls.url_refresh = reverse('account:token_refresh')
    def test_login_for_get_tokens(self):
        response = self.client.post(self.url_token,self.login_data)
        response_json = response.json()
        self.assertEqual(response.status_code,200)
        self.assertIn('refresh',response_json)
        self.assertIn('access',response_json)

    def test_invalid_login_for_get_tokens(self):
        invalid_login_data = {'username':'dwdwd','password':'hrpir'}
        response = self.client.post(self.url_token, invalid_login_data)
        response_json = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response_json)


    def test_valid_refresh_token(self):
        _response = self.client.post(self.url_token, self.login_data)
        refresh_token = _response.json()['refresh']

        response = self.client.post(self.url_refresh,{'refresh':refresh_token})
        response_json = response.json()

        self.assertEqual(response.status_code,200)
        self.assertIn('refresh', response_json)
        self.assertIn('access', response_json)


    def test_invalid_refresh_token(self):
        refresh_token = 'X' * 20

        response = self.client.post(self.url_refresh, {'refresh': refresh_token})
        response_json = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response_json)

    def test_valid_access_token(self):
        _response = self.client.post(self.url_token, self.login_data)
        access_token = _response.json()['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url_test)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{'status':'OK'})



    def test_invalid_access_token(self):
        access_token = 'X' * 20

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url_test)
        response_json = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail',response_json)
        self.assertIn('Given token not valid',response.json()['detail'])

    def test_without_access_token(self):
        response = self.client.get(self.url_test)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'detail': 'Authentication credentials were not provided.'})

