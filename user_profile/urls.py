from django.urls import path
from django.views.generic import TemplateView

from rest_framework.routers import SimpleRouter

from user_profile.views import UserProfileViewSet, ConfirmChangeEmail, ProfileSettingsView

router = SimpleRouter()
router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path(
        'confirm_change_email/<str:uid>/<str:token>/<str:email>/',
        ConfirmChangeEmail.as_view(),
        name='confirm_change_email'
    ),
    path(
        'profile_settings/<int:id>/',
        ProfileSettingsView.as_view(),
        name='profile_settings'
    )
]

urlpatterns += router.urls
