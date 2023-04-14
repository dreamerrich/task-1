from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Task, Permission

class IsAdminOrReadOnly(BasePermission):
   
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
    
# class IsAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             user = request.user

#             user_role = Permission.objects.get(name=user)
#            
#             if user_role and user_role.can_create:
#                 return True
            
#             return False
        
#         return True
    
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            id = view.kwargs.get('pk')

            user = request.user
            user_role = Permission.objects.filter(name=user).get(project=id)
            if user_role and user_role.can_delete:
                return True

            return False

        return True
    
    def has_permission(self, request, view):
        if request.method == 'PUT':
            id = view.kwargs.get('pk')

            user = request.user
            user_role = Permission.objects.filter(name=user).get(project=id)
            if user_role and user_role.can_edit:
                return True

            return False

        return True
    
    def has_permission(self, request, view):
        if request.method == 'PATCH':
            id = view.kwargs.get('pk')

            user = request.user
            user_role = Permission.objects.filter(name=user).get(project=id)
            if user_role and user_role.can_edit:
                return True

            return False

        return True
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            user = request.user

            user_role = Permission.objects.get(name=user)
            if user_role and user_role.can_create:
                return True
            
            return False
        
        return True