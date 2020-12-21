from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from user_profile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Отображение профиля пользователя в панели администратора"""

    def avatar_url(self, obj) -> SafeString:
        """Отображение на аватара пользователя в панели администратора"""

        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="80" height="80" />')
        return mark_safe(f'<img src="/media/default_image_for_user_profile.png" width="80" height="80" />')

    list_display = ('id', 'user', 'avatar_url', 'phone', 'city')
