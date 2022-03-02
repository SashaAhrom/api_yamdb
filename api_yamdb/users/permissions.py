from rest_framework import permissions

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff and request.user.role == 'moderator'


class IsAuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or (request.user.is_staff and request.user.role == 'admin')
        )
