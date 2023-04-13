from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Task, Permission

class IsAdminOrReadOnly(BasePermission):
   
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
    
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user in SAFE_METHODS:
            return True
        return request.user and request.user.is_active
    
    # def has_permission(self, request, view):
    #     if request.user == Task.user:
    #         print("in if task")
    #         if Permission.can_delete == True:
    #             print("in if per")
    #             return True
    #     return request.user and request.user.is_active
    
    # def has_permission(self, request, view):
    #     if request.user == Task.user:
    #         Permission.can_edit == True
    #         return True
    #     return request.user and request.user.is_active