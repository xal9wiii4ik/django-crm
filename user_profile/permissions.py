from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    """Permission class для владеьца объекта или администратора"""

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user or
                    (request.user.is_staff and request.method == 'GET'))
