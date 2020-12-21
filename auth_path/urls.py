from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from auth_path.views import (
    RegistrationView,
    ActivationView,
    LogInView,
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    path('sign_up/', RegistrationView.as_view(), name='sign_up'),
    path('activation/<str:uid>/<str:token>/', ActivationView.as_view(), name='activation'),
    path('login/', LogInView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
]
