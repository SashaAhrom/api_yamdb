from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Custom permission for users with admin role."""

    message = 'Доступ только для администраторов и выше!'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Access to safe points is allowed to everyone to
    the rest only user, admin and moderator.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or
                request.user.role in ('admin', 'moderator') or
                request.user.is_superuser)
