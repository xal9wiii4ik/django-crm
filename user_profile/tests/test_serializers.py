from django.contrib.auth.models import User
from django.db.models import F
from django.test import TestCase

from user_profile.models import UserProfile
from user_profile.serializer import UserProfileModelSerializer


class UserProfileSerializerTestCase(TestCase):
    """Test Case для тестирования сериалайзера профиля пользователя"""

    def test_ok(self):
        self.password = '123123'
        user = User.objects.create(
            username='user',
            email='email',
            password=self.password,
            is_staff=True
        )
        user_1 = User.objects.create(
            username='username',
            email='email_1',
            password=self.password
        )

        user_profile = UserProfile.objects.create(user=user,
                                                  phone='123',
                                                  city='Moscow')
        user_profile = UserProfile.objects.create(user=user_1,
                                                  street='Street')
        user_profiles = UserProfile.objects.all().annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            email=F('user__email'),
            username=F('user__username'),
            is_staff=F('user__is_staff')
        )
        data = UserProfileModelSerializer(user_profiles, many=True).data
        expected_data = [
            {
                'first_name': '',
                'last_name': '',
                'email': 'email',
                'username': '',
                'is_staff': '',
                'user': user.id,
                'phone': '123',
                'street': '',
                'city': 'Moscow',
                'region': '',
                'avatar': None
            },
            {
                'first_name': '',
                'last_name': '',
                'email': 'email_1',
                'username': '',
                'is_staff': '',
                'user': user_1.id,
                'phone': '',
                'street': 'Street',
                'city': '',
                'region': '',
                'avatar': None
            }
        ]
