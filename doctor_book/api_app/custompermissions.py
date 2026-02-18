from rest_framework.permissions import BasePermission

class My_permission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.groups.filter(name='admin_user').exists()
                
        return False
    
class Patient_permission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'DELETE']:
            return request.user.groups.filter(name='admin_user').exists()
        
        if request.method == 'POST':
            return True
        
        return False
