from django.contrib.auth.models import Group
from rest_framework import permissions


def is_in_group(user, group_name):
    """
    验证用户是否在某个组中
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class HasGroupPermission(permissions.BasePermission):
    """
    对不同的请求方法做不同组策略的权限控制
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(view, "required_groups", {})

        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])

        # Return True if the user has any of the required groups or is staff.
        permission = any(
            [is_in_group(request.user, group_name) if group_name != "__all__" else True for group_name in required_groups]
            ) or (request.user and request.user.is_staff)
            
        return permission