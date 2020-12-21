from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from rest_framework.serializers import ValidationError

from auth_path.services_serializer import verification_password, verification_unique_email, verification_unique_username
from auth_path.services_view import (
    _get_web_url,
    _create_unique_uid_and_token,
    _verification_uid_and_token,
    _get_verification_data_or_404,
    _delete_uid_and_token,
)
from django_crm import settings
from user_profile.models import UserProfile


def get_user_profile_data(id: int) -> dict:
    """Получение данных пользователя"""

    user_profile = UserProfile.objects.get(id=id)
    user_profile_data = {
        'username': user_profile.user.username,
        'first_name': user_profile.user.first_name,
        'last_name': user_profile.user.last_name,
        'email': user_profile.user.email,
        'phone': user_profile.phone,
        'street': user_profile.street,
        'city': user_profile.city,
        'region': user_profile.region,
        'avatar': user_profile.avatar.url
    }
    return user_profile_data


def update_fields_in_user_model(data: dict, request, id: int) -> None or dict:
    """Обновление полей модель юзера(first_name, last_name, etc.)"""

    owner_of_user_profile = UserProfile.objects.get(id=id).user
    keys = data.keys()
    fields = ''
    print(keys)

    if 'last_name' in keys and owner_of_user_profile.last_name != data['last_name']:
        owner_of_user_profile.last_name = data['last_name']
        fields += ' last_name'
    if 'first_name' in keys and owner_of_user_profile.first_name != data['first_name']:
        owner_of_user_profile.first_name = data['first_name']
        fields += ' first_name'
    if 'password' in keys:
        verification_password(value=data['password'])
        owner_of_user_profile.password = make_password(data['password'])
        fields += ' password'
    if 'username' in keys and owner_of_user_profile.username != data['username']:
        try:
            verification_unique_username(value=data['username'])
            owner_of_user_profile.username = data['username']
            fields += ' username'
        except ValidationError:
            pass
    if 'email' in keys and owner_of_user_profile.email != data['email']:
        try:
            verification_unique_email(value=data['email'])
            new_data = _create_unique_uid_and_token(user=owner_of_user_profile)
            url = _get_web_url(is_secure=request.is_secure(),
                               host=request.get_host(),
                               url=f'/user/confirm_change_email/{new_data["uid"]}/{new_data["token"]}/{data["email"]}')
            send_mail(subject='Change Email',
                      message=f'Please click here\n {url}',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[owner_of_user_profile.email],
                      fail_silently=False)
        except ValidationError:
            pass
    if fields != '':
        send_mail(subject='Your privacy settings has been changed',
                  message=f'Your {fields} has been changed',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[owner_of_user_profile.email],
                  fail_silently=False)
        owner_of_user_profile.save()


def confirm_change_email(uid: str, token: str, email: str) -> bool:
    """Подтверждение смены почты пользователя"""

    if _verification_uid_and_token(uid=uid, token=token):
        verification_data = _get_verification_data_or_404(
            uid=uid,
            token=token
        )
        verification_data['uid_object'].user.email = email
        verification_data['uid_object'].user.save()
        _delete_uid_and_token(uid_object=verification_data['uid_object'],
                              token_object=verification_data['token_object'])
        return True
    else:
        return False
