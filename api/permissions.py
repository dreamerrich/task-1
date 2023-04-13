from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Task, Permission

class IsAdminOrReadOnly(BasePermission):
   
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
    
class IsAuthenticated(BasePermission):
    def has_add_permission(self, request, obj=None):
        if request.user == Task.user and Permission.can_create:
            return True
        return request.user and request.user.is_active
    
    def has_delete_permission(self, request, obj=None):
        if request.user == Task.user and Permission.can_delete:
            return True
        return request.user and request.user.is_active
    
    def has_change_permission(self, request, obj=None):
        if request.user == Task.user:
            return True
        return request.user and request.user.is_active