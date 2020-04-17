from rest_framework.permissions import BasePermission 

class VipPermission(BasePermission):
    message = "u shall not pass！"
    def has_permission(self,request,view):
        if request.user.user_type == 1:
            return False
        return True