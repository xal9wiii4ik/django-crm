from django.contrib.auth.models import User
from django.test import TestCase

from auth_path.serializers import (
    RegistrationSerializer,
    LogInSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class RegistrationSerializerTestCase(TestCase):
    """Test registration serializer """

    def test_valid_data(self):
        """Valid data"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': 'Password1',
            'repeat_password': 'Password1',
        }
        self.assertTrue(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_mail(self):
        """Un valid data"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'emailmail.ru',
            'username': 'username',
            'password': 'Password1',
            'repeat_password': 'Password1',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_less_then_8_characters(self):
        """Un valid password less_then_8_characters"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': 'pass',
            'repeat_password': 'pass',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_capital_letter(self):
        """Un valid password with_out_capital_letter"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': '12345678',
            'repeat_password': '12345678',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_numbers(self):
        """un valid password with_out_numbers"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': 'asdAASDa',
            'repeat_password': 'asdAASDa',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())


class LoginSerializerTestCase(TestCase):
    """Test log in serializer"""

    def setUp(self):
        User.objects.create(username='username', email='username@mail.ru')

    def test_valid_data(self):
        """Valid data"""

        data = {
            'username': 'username@mail.ru',
            'password': 'password'
        }
        serializer = LogInSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual('username', serializer.data['username'])

    def test_un_valid_data_mail(self):
        """un valid data"""

        data = {
            'username': 'userna@mail.ru',
            'password': 'password'
        }
        serializer = LogInSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ForgotPasswordSerializerSerializerTestCase(TestCase):
    """Test forgot password serializer"""

    def setUp(self):
        User.objects.create(username='username', email='username@mail.ru')

    def test_valid_data(self):
        """Valid data"""

        data = {
            'email': 'username@mail.ru'
        }
        self.assertTrue(ForgotPasswordSerializer(data=data).is_valid())

    def test_un_valid_data_mail(self):
        """Un valid data"""

        data = {
            'email': 'usern@mail.ru'
        }
        self.assertFalse(ForgotPasswordSerializer(data=data).is_valid())


class ResetPasswordSerializerTestCase(TestCase):
    """Test reset password serializer"""

    def test_valid_data(self):
        """Valid data"""

        data = {
            'password': 'Password1',
            'repeat_password': 'Password1'
        }
        self.assertTrue(ResetPasswordSerializer(data=data).is_valid())

    def test_un_valid_password_less_then_8_characters(self):
        """Un valid data"""

        data = {
            'password': 'pass',
            'repeat_password': 'pass',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_capital_letter(self):
        """Un valid data"""

        data = {
            'password': '12345678',
            'repeat_password': '12345678',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())


def test_un_valid_password_with_out_numbers(self):
    """Un valid data"""

    data = {
        'password': 'asdAASDa',
        'repeat_password': 'asdAASDa',
    }
    self.assertFalse(RegistrationSerializer(data=data).is_valid())
