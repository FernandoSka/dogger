from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            request.user.customer.owner
            return True
        except Exception as e:
            return False

class IsWalker(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            request.user.customer.walker
            return True
        except Exception as e:
            return False