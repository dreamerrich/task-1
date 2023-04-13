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
#             print("🚀 ~ file: permissions.py:19 ~ user:", user)

#             user_role = Permission.objects.get(name=user)
#             print("🚀 ~ file: permissions.py:20 ~ role:", user_role)
#             if user_role and user_role.can_create:
#                 print(">>>>>>>>>>if inside>>>>>>>>>>")
#                 return True
            
#             return False
        
#         return True
    
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            id = view.kwargs.get('pk')
            print("🚀 ~ file: permissions.py:33 ~ id:", id)

            user = request.user
            user_role = Permission.objects.filter(name=user).get(project=id)
            print("🚀 ~ file: permissions.py:26 ~ user_role:", user_role)
            if user_role and user_role.can_delete:
                print(">>>>>>>>>>if inside>>>>>>>>>>")
                return True

            return False

        return True
    
    def has_permission(self, request, view):
        if request.method == 'PUT':
            id = view.kwargs.get('pk')
            print("🚀 ~ file: permissions.py:33 ~ id:", id)

            user = request.user
            user_role = Permission.objects.filter(name=user).get(project=id)
            print("🚀 ~ file: permissions.py:26 ~ user_role:", user_role)
            if user_role and user_role.can_edit:
                print(">>>>>>>>>>if inside>>>>>>>>>>")
                return True

            return False

        return True
    
    def has_permission(self, request, view):
        if request.method == 'PATCH':
            id = view.kwargs.get('pk')
            print("🚀 ~ file: permissions.py:33 ~ id:", id)

            user = request.user
            user_role = Permission.objects.filter(name=user).get(project=id)
            print("🚀 ~ file: permissions.py:26 ~ user_role:", user_role)
            if user_role and user_role.can_edit:
                print(">>>>>>>>>>if inside>>>>>>>>>>")
                return True

            return False

        return True
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            user = request.user
            print("🚀 ~ file: permissions.py:19 ~ user:", user)

            user_role = Permission.objects.get(name=user)
            print("🚀 ~ file: permissions.py:20 ~ role:", user_role)
            if user_role and user_role.can_create:
                print(">>>>>>>>>>if inside>>>>>>>>>>")
                return True
            
            return False
        
        return True