from django.contrib.auth.models import Permission
from rest_framework.permissions import BasePermission

from accounting.models import Organization


class CanAddStaff(BasePermission):

    def has_permission(self, request, view):
        organization_id = view.kwargs.get('organization_id', 0)
        staff = request.user.user_profile
        try:
            staff.organization.get(pk=organization_id)
            return staff.user.has_perm('accounting.can_add_staff')
        except Organization.DoesNotExist:
            return False
