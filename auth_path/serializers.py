from rest_framework import serializers

from auth_path.services_serializer import (
    verification_password,
    verification_exist_email,
    verification_unique_email,
    verification_email_and_return_username,
    verification_unique_username
)


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя"""

    first_name = serializers.CharField(max_length=25, required=True)
    last_name = serializers.CharField(max_length=25, required=True)
    email = serializers.EmailField(max_length=60, required=True)
    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)
    repeat_password = serializers.CharField(max_length=60, required=True)

    def validate_username(self, value: str) -> str:
        """Валидация имени пользователя"""

        return verification_unique_username(value=value)

    def validate_email(self, value: str) -> str:
        """Валидация почты"""

        return verification_unique_email(value=value)

    def validate_password(self, value: str) -> str:
        """Валидация пароля"""

        return verification_password(value=value)


class LogInSerializer(serializers.Serializer):
    """Сериалайзер для входа в аккаунт и получения токена"""

    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)

    def validate_username(self, value: str) -> str:
        """Валидация почты и проверка на наличие пользователя в базе"""

        return verification_email_and_return_username(value=value)


class ForgotPasswordSerializer(serializers.Serializer):
    """Сериалайзер для восстановления пароля"""

    email = serializers.EmailField(max_length=60, required=True)

    def validate_email(self, value: str) -> str:
        """Валидация почты и проверка на наличие пользователя в базе"""

        return verification_exist_email(value=value)


class ResetPasswordSerializer(serializers.Serializer):
    """Суриалайзер для смены пароля"""

    password = serializers.CharField(max_length=60, required=True)
    repeat_password = serializers.CharField(max_length=60, required=True)

    def validate_password(self, value: str) -> str:
        """Валидация пароля"""

        return verification_password(value=value)
