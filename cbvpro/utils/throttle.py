from rest_framework.throttling import BaseThrottle,SimpleRateThrottle

class VisitThrottle(SimpleRateThrottle):
    scope = "Visitor"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
    # 根据ip控制

class UserThrottle(SimpleRateThrottle):

    scope = "User"
    # scope和setting中对应
    def get_cache_key(self, request, view):

        # 唯一表示是用户名
        # return request.user.username
        # auth时 把username赋给了request
        return self.user.username