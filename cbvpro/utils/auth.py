from rest_framework import exceptions
from cbvpro.models import UserToken,UserInfo
from rest_framework.authentication import BaseAuthentication
# lo/cbv/v1/info/
class Autht(BaseAuthentication):
    # 常用
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest_framework内部将会将整个两个字段赋值给request，以供后续操作使用 前者给user 后者给auth
        return (token_obj.user, token_obj)

	# 这个方法一般用不到
    def authenticate_header(self, request):
        pass

# 必须传递一个token才能获取想要的东西