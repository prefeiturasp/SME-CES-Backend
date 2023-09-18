from rest_framework.permissions import BasePermission
from .constants import GRUPO_NIVEL_API


class IsAPIUser(BasePermission):
    def get_required_permissions(self):
        return [GRUPO_NIVEL_API]

    def has_permission(self, request, view):
        user_groups = request.user.groups
        perms = self.get_required_permissions()
        return user_groups.filter(name__in=perms)
