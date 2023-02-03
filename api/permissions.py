from rest_framework import permissions


class AdminOrAnyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True
        elif view.action == "create":
            if request.user.is_authenticated:
                return request.user.is_superuser or request.user.role == 'admin'
            return False
        elif view.action in ['update', 'partial_update', 'destroy']:
            if request.user.is_authenticated:
                return request.user.is_superuser or request.user.role == 'admin'
            return False
        else:
            return False


class AdminOrAnyOrAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True
        elif view.action == "create":
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            if request.user.is_authenticated:
                return obj.author == request.user or \
                   request.user.role == 'admin' or \
                   request.user.role == 'moderator' or \
                   request.user.is_superuser
            return False
        else:
            return False


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'
        return False
