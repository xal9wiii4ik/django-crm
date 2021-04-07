from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from auth_path.services_serializer import (
    verification_password,
    verification_unique_email,
    verification_unique_username,
    verification_exist_email,
    verification_email_and_return_username
)


class ServicesSerializerTestCase(TestCase):
    """Test for services of serializer"""

    def setUp(self):
        self.user = User.objects.create(username='user',
                                        email='email@mail.ru')

    def test_verification_password_un_valid_least_8(self):
        """validation password"""

        try:
            verification_password(value='1234567')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_un_valid_only_numbers(self):
        """validation password"""

        try:
            verification_password(value='12345678')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_un_valid_no_contain_upper_latter(self):
        """validation password"""

        try:
            verification_password(value='12345678')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_un_valid_no_contain_number(self):
        """validation password"""

        try:
            verification_password(value='aaaaaaaAAAAA')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_valid(self):
        """validation password"""

        self.assertTrue(check_password(password='aaaaaaaAAAAA1',
                                       encoded=verification_password(value='aaaaaaaAAAAA1')))

    def test_verification_unique_email(self):
        """validation email"""

        self.assertEqual('exist@mail.ru',
                         verification_unique_email('exist@mail.ru'))

    def test_verification_exist_email(self):
        """validation email exist"""

        self.assertEqual(self.user.email,
                         verification_exist_email(self.user.email))

    def test_verification_unique_username(self):
        """validation username"""

        self.assertEqual('unique_username',
                         verification_unique_username(value='unique_username'))

    def test_verification_exist_username(self):
        """validation email exist"""

        try:
            verification_unique_username(value=self.user.username)
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_email_and_return_username(self):
        """validation username and return username"""

        self.assertEqual(self.user.username,
                         verification_email_and_return_username(value=self.user.email))
