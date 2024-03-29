from apps.accounts.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You not is Owner'

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view,  obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.author

class OwnerCommentOnly(BasePermission):
    message = 'This Comment Not for You'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
