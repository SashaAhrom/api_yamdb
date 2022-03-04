from rest_framework import permissions


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
