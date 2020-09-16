from rest_framework import permissions
import api.models as am


class IsOwner(permissions.BasePermission):
    """
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            email = request.user.email
        is_permitted = False
        if request.method:
            try:
                user = am.AppUser.objects.filter(email=email).exists()
                if user:
                    is_permitted = True
                else:
                    is_permitted = False
            except am.AppUser.DoesNotExist:
                is_permitted = False
        return is_permitted
