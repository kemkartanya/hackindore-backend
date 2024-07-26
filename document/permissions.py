from rest_framework import permissions as rest_permissions


class CanAccessDocument(rest_permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        base_permission = super().has_object_permission(request, view, obj)

        if obj.user == request.user:
            return True

        if base_permission:
            return True

        return False
