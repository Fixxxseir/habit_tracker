from rest_framework import permissions, status


class IsAdminOrIsStaff(permissions.BasePermission):
    """
    Права доступа и admin и staff
    """
    message = {
        "forbidden": "Доступ запрещен",
    }
    code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser


class OwnerHabitPermission(permissions.BasePermission):
    """
    Права доступа только владельцу
    """
    message = {
        "forbidden": "Доступ запрещен",
    }
    code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
