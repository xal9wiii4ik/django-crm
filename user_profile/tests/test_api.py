import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase

from user_profile.models import UserProfile


class UserProfileApiTestCase(APITestCase):
    """Api test case для тестирования функционала профиля пользователя"""

    def setUp(self) -> None:
        self.url_token = reverse(viewname='auth_path:token')

        self.password = '123123'
        self.user = User.objects.create(
            username='user',
            email='email',
            password=make_password(password=self.password),
            is_staff=True
        )
        data = {
            'username': self.user.username,
            'password': self.password
        }
        json_data = json.dumps(obj=data)
        self.token = 'Token ' + self.client.post(
            path=self.url_token,
            data=json_data,
            content_type='application/json'
        ).data['access']

        self.user_1 = User.objects.create(
            username='username',
            email='email_1',
            password=make_password(password=self.password)
        )
        data_1 = {
            'username': self.user_1.username,
            'password': self.password
        }
        json_data_1 = json.dumps(obj=data_1)
        self.token_1 = 'Token ' + self.client.post(
            path=self.url_token,
            data=json_data_1,
            content_type='application/json'
        ).data['access']

        self.user_2 = User.objects.create(
            username='username_2',
            email='email_2',
            password=make_password(password=self.password)
        )
        data_2 = {
            'username': self.user_2.username,
            'password': self.password
        }
        json_data_2 = json.dumps(obj=data_2)
        self.token_2 = 'Token ' + self.client.post(
            path=self.url_token,
            data=json_data_2,
            content_type='application/json'
        ).data['access']

        self.user_profile_1 = UserProfile.objects.create(user=self.user_1)

    def test_get_list(self) -> None:
        """Тест для получения списка профилей пользователей"""

        url = reverse(viewname='user:userprofile-list')
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)

    def test_create(self) -> None:
        """Тест для создания профиля пользователя"""

        url = reverse(viewname='user:userprofile-list')
        response = self.client.post(path=url)
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)

    def test_get_detail_owner(self) -> None:
        """Тест для получения профиля пользователя владельцем"""

        url = reverse(viewname='user:userprofile-detail', args=(self.user_profile_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_detail_not_owner(self) -> None:
        """Тест для получения профиля пользователя не владельцем"""

        url = reverse(viewname='user:userprofile-detail', args=(self.user_profile_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_get_detail_not_owner_but_staff(self) -> None:
        """Тест для получения профиля пользователя не владельцем а администратором"""

        url = reverse(viewname='user:userprofile-detail', args=(self.user_profile_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_update_owner(self) -> None:
        """Тест для обновления профиля пользователя владельцем кроме аватарки"""

        self.assertEqual(first='', second=self.user_profile_1.phone)
        url = reverse(viewname='user:userprofile-detail', args=(self.user_profile_1.id,))
        data = {
            'phone': 'new_phone'
        }
        json_data = json.dumps(obj=data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.user_profile_1.refresh_from_db()
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(first=data['phone'], second=self.user_profile_1.phone)

    def test_update_not_owner_but_staff(self) -> None:
        """Тест для обновления профиля пользователя не владельцем а администратором кроме аватарки"""

        self.assertEqual(first='', second=self.user_profile_1.phone)
        url = reverse(viewname='user:userprofile-detail', args=(self.user_profile_1.id,))
        data = {
            'phone': 'new_phone'
        }
        json_data = json.dumps(obj=data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.user_profile_1.refresh_from_db()
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=data['phone'], second=self.user_profile_1.phone)

    def test_update_not_owner(self) -> None:
        """Тест для обновления профиля пользователя не владельцем кроме аватарки"""

        self.assertEqual(first='', second=self.user_profile_1.phone)
        url = reverse(viewname='user:userprofile-detail', args=(self.user_profile_1.id,))
        data = {
            'phone': 'new_phone'
        }
        json_data = json.dumps(obj=data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.user_profile_1.refresh_from_db()
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first='', second=self.user_profile_1.phone)
