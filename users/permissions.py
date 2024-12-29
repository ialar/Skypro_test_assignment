from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """Проверяет, является ли пользователь (сотрудник) активным."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
