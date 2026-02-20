from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Admin role required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="admin").exists()
        )


class IsEditorOrAdmin(BasePermission):
    message = "Editor or Admin role required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name__in=["admin", "editor"]).exists()
        )


class IsAnyRole(BasePermission):
    message = "Authentication with an assigned role is required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name__in=["admin", "editor", "viewer"]).exists()
        )
