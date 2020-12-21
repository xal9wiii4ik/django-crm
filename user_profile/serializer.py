from rest_framework import serializers

from user_profile.models import UserProfile


class UserProfileModelSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели профиля пользователя"""

    first_name = serializers.CharField(max_length=40, required=False)
    last_name = serializers.CharField(max_length=40, required=False)
    email = serializers.EmailField(max_length=40, required=False)
    username = serializers.CharField(max_length=60, required=False)
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email',
                  'id', 'username', 'phone', 'street',
                  'city', 'region', 'avatar', 'is_staff']
