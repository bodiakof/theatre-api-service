from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Grants read-only access to authenticated users.
    Grants full access to admin users.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if the user has permission to access the resource."""
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (request.method in SAFE_METHODS or user.is_staff)
        )
