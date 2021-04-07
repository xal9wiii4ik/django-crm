from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from auth_path.models import Uid
from auth_path.services_view import (
    _get_verification_data_or_404,
    _get_web_url,
    _create_unique_uid_and_token,
    _verification_uid_and_token,
    _delete_uid_and_token,
)


def get_request():
    url = reverse('auth_path:login')
    factory = APIRequestFactory()
    return factory.get(url)


class ServicesTestCase(TestCase):
    """Test for services of views"""

    def setUp(self):
        password = make_password(password='password')
        self.user = User.objects.create(
            username='username',
            email='email@mail.ru',
            password=password,
            is_active=True)
        self.uid = Uid.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)

        password_1 = make_password(password='password_1')
        self.user_1 = User.objects.create(
            username='username_1',
            email='email_1@mail.ru',
            password=password_1,
            is_active=True)
        self.uid_1 = Uid.objects.create(user=self.user_1)
        self.token_1 = Token.objects.create(user=self.user_1)

    def test_delete_object_or_uid_and_token(self):
        """delete uid and token"""

        self.assertEqual(2, Uid.objects.all().count())
        self.assertEqual(2, Token.objects.all().count())
        _delete_uid_and_token(uid_object=self.uid, token_object=self.token)
        self.assertEqual(1, Token.objects.all().count())
        self.assertEqual(1, Uid.objects.all().count())

    def test_get_verification_data_or_404_valid(self):
        """getting uid and token valid data"""

        data = _get_verification_data_or_404(uid=self.uid.uid,
                                             token=self.token.key)
        self.assertEqual(self.uid, data['uid_object'])
        self.assertEqual(self.token, data['token_object'])

    def test_get_verification_data_or_404_un_valid_token(self):
        """getting uid and token un valid data"""

        try:
            _get_verification_data_or_404(uid='self.uid.uid',
                                          token=self.token.key)
        except Http404:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_get_verification_data_or_404_un_valid_uid(self):
        """getting uid and token valid data"""

        try:
            _get_verification_data_or_404(uid=self.uid.uid,
                                          token='self.token.key')
        except Http404:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_get_web_url_equal(self):
        """Getting true link"""

        request = get_request()
        url = _get_web_url(is_secure=request.is_secure(),
                           host=request.get_host(),
                           url='auth/sign_up/')
        self.assertEqual('http://testserverauth/sign_up/', url)

    def test_get_web_url_not_equal(self):
        """Getting un true link"""

        request = get_request()
        url = _get_web_url(is_secure=request.is_secure(),
                           host=request.get_host(),
                           url='auth/sign_up/')
        self.assertNotEqual('http://local/sign_up/', url)

    def test_create_unique_uid_and_exist_token(self):
        """Create uid and token"""

        self.uid.delete()
        self.token.delete()
        data = _create_unique_uid_and_token(user=self.user)
        expected_data = {
            'uid': Uid.objects.get(user=self.user).uid,
            'token': Token.objects.get(user=self.user).key
        }
        self.assertEqual(expected_data, data)

    def test_create_exist_uid_and_unique_token(self):
        """Create un valid uid and token"""

        try:
            _create_unique_uid_and_token(user=self.user)
        except IntegrityError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_uid_and_token_valid(self):
        """Check uid and token for true"""

        self.assertTrue(_verification_uid_and_token(uid=self.uid.uid,
                                                    token=self.token.key))

    def test_verification_uid_and_token_un_valid_uid(self):
        """Check uid and token for not true"""

        self.assertFalse(_verification_uid_and_token(uid=self.uid_1.uid,
                                                     token=self.token.key))

    def test_verification_uid_and_token_un_valid_token(self):
        """Check uid and token for not true"""

        self.assertFalse(_verification_uid_and_token(uid=self.uid.uid,
                                                     token=self.token_1.key))
