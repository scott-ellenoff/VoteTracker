from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow user or admin to edit itself
    """

    def has_object_permission(self, request, view, user_obj):
        return user_obj == request.user or request.user.is_staff

class IsSelf(permissions.BasePermission):
    """
    Custom permission to only allow user to edit itself.
    """

    def has_object_permission(self, request, view, user_obj):
        return user_obj == request.user