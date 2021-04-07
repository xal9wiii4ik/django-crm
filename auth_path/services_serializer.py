from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import serializers


def verification_password(value: str) -> str:
    """Check password"""

    if len(value) >= 8:
        if any((c in set('QAZWSXEDCRFVTGBYHNUJMIKOLP')) for c in value):
            if any((f in set('1234567890') for f in value)):
                return make_password(value)
            else:
                raise serializers.ValidationError('Password must contain at least 1 number')
        else:
            raise serializers.ValidationError('Password must contain at least 1 uppercase letter')
    else:
        raise serializers.ValidationError('Password must have to have at least 8 characters')


def verification_unique_email(value: str) -> str:
    """Checking unique of email"""

    user = User.objects.filter(email=value)
    if len(user) == 0:
        return value
    else:
        raise serializers.ValidationError('User with given credentials already exist')


def verification_unique_username(value: str) -> str:
    """Checking unique of username"""

    user = User.objects.filter(username=value)
    if len(user) == 0:
        return value
    else:
        raise serializers.ValidationError('User with given credentials already exist')


def verification_exist_email(value: str) -> str:
    """Checking exist email"""

    user = User.objects.filter(email=value)
    if len(user) != 0:
        return value
    else:
        raise serializers.ValidationError('User with given credentials are not found')


def verification_email_and_return_username(value: str) -> str:
    """Checking exist email and return value"""

    user = User.objects.filter(email=value)
    if len(user) != 0:
        return user[0].username
    else:
        raise serializers.ValidationError('User with given credentials are not found')
