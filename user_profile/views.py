from django.db.models import F

from rest_framework import renderers, parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user_profile.permissions import IsOwnerOrStaff
from user_profile.models import UserProfile
from user_profile.serializer import UserProfileModelSerializer
from user_profile.services_view import (
    update_fields_in_user_model,
    confirm_change_email,
    get_user_profile_data,
)


class UserProfileViewSet(ModelViewSet):
    """ViewSet для профиля пользователя"""

    queryset = UserProfile.objects.all().annotate(
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email'),
        username=F('user__username'),
        is_staff=F('user__is_staff')
    )
    serializer_class = UserProfileModelSerializer
    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    permission_classes = (IsOwnerOrStaff,)
    template_name = 'auth/login.html'  # default template for test cases

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return Response(
                data={'error': f'method {request.method} not allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return Response(
            data={'error': f'method {request.method} not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def retrieve(self, request, *args, **kwargs):
        response = super(UserProfileViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response(data={'data': response.data}, template_name='user/main.html')
        return response

    def destroy(self, request, *args, **kwargs):
        return Response(
            data={'error': f'method {request.method} not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def create(self, request, *args, **kwargs):
        return Response(
            data={'error': f'method {request.method} not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        response = super(UserProfileViewSet, self).update(request, *args, **kwargs)
        update_fields_in_user_model(data=request.data,
                                    request=request,
                                    id=response.data['id'])
        if request.accepted_renderer.format == 'html':
            return Response(data={},
                            status=status.HTTP_200_OK)
        return response


class ProfileSettingsView(APIView):
    """Настройки пользователя"""

    renderer_classes = (renderers.TemplateHTMLRenderer,)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    permission_classes = (IsOwnerOrStaff,)

    def get(self, request, id):
        return Response(data={'id': id, 'user_profile_data': get_user_profile_data(id=id)},
                        status=status.HTTP_200_OK,
                        template_name='user/profile_settings.html')


class ConfirmChangeEmail(APIView):
    """Подтверждение смены пароля у пользователя"""

    def get(self, request, uid: str, token: str, email: str):
        if confirm_change_email(uid=uid, token=token, email=email):
            return Response(data={'ok': 'Your email has been changed'},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Un valid uid or token'},
                            status=status.HTTP_400_BAD_REQUEST)
