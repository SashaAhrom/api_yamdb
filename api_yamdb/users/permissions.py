from rest_framework import permissions

class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and request.user.role == 'admin'


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or (request.user.is_staff and request.user.role == 'admin')
        )
