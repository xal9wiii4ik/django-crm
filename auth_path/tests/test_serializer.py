from django.contrib.auth.models import User
from django.test import TestCase

from auth_path.serializers import (
    RegistrationSerializer,
    LogInSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class RegistrationSerializerTestCase(TestCase):
    """Тест для сериалайзера регистрации"""

    def test_valid_data(self):
        """Тест сериалайзера регистрации валидные данные"""

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
        """Тест сериалайзера регистрации не валидный майл"""

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
        """Тест сериалайзера регистрации не валидный пароль
        меньше 8 символов"""

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
        """Тест сериалайзера регистрации не валидный пароль
        без заглавной буквы"""

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
        """Тест сериалайзера регистрации не валидный пароль
        без цифр"""

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
    """Тест для сериалайзера авторизации"""

    def setUp(self):
        User.objects.create(username='username', email='username@mail.ru')

    def test_valid_data(self):
        """Тест сериалайзера авторизации валидные данные"""

        data = {
            'username': 'username@mail.ru',
            'password': 'password'
        }
        serializer = LogInSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual('username', serializer.data['username'])

    def test_un_valid_data_mail(self):
        """Тест сериалайзера авторизации не валидные данные
        почта пользователя"""

        data = {
            'username': 'userna@mail.ru',
            'password': 'password'
        }
        serializer = LogInSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ForgotPasswordSerializerSerializerTestCase(TestCase):
    """Тест для сериалайзера забыл пароль"""

    def setUp(self):
        User.objects.create(username='username', email='username@mail.ru')

    def test_valid_data(self):
        """Тест сериалайзера забыл пароль валидные данныe"""

        data = {
            'email': 'username@mail.ru'
        }
        self.assertTrue(ForgotPasswordSerializer(data=data).is_valid())

    def test_un_valid_data_mail(self):
        """Тест сериалайзера забыл пароль не валидные данные
        почта пользователя"""

        data = {
            'email': 'usern@mail.ru'
        }
        self.assertFalse(ForgotPasswordSerializer(data=data).is_valid())


class ResetPasswordSerializerTestCase(TestCase):
    """Тест для сериалайзера замена пароля"""

    def test_valid_data(self):
        """Тест для сериалайзера замена пароля валидные данные"""

        data = {
            'password': 'Password1',
            'repeat_password': 'Password1'
        }
        self.assertTrue(ResetPasswordSerializer(data=data).is_valid())

    def test_un_valid_password_less_then_8_characters(self):
        """Тест сериалайзера замена пароля не валидный пароль
        меньше 8 символов"""

        data = {
            'password': 'pass',
            'repeat_password': 'pass',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_capital_letter(self):
        """Тест сериалайзера замена пароля не валидный пароль
        без заглавной буквы"""

        data = {
            'password': '12345678',
            'repeat_password': '12345678',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_numbers(self):
        """Тест сериалайзера замена пароля не валидный пароль
        без цифр"""

        data = {
            'password': 'asdAASDa',
            'repeat_password': 'asdAASDa',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())
