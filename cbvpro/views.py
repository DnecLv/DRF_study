from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.views import View
from django.utils.decorators import method_decorator

order_dict ={
    1:{
        'name': 'cushu',
        'age': 18
    },
    2:{
        'name': 'sqs',
        'age': 55
    }
}
# Create your views here.




@method_decorator(csrf_exempt,name='dispatch')
class TurView(View): 
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET')

from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework import request
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning

from rest_framework.parsers import JSONParser,FormParser
class Autht(BaseAuthentication):
    # 常用
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest_framework内部将会将整个两个字段赋值给request，以供后续操作使用 前者给user 后者给auth
        return (token_obj.user, token_obj)

	# 这个方法一般用不到
    def authenticate_header(self, request):
        pass


class Visit:
    def allow_request(self, request, view):
        return False # False 表示被限制
    
    def wait(self):
        return None

# apiview可以继承多个类
# lo/cbv/info/

class GetInfo(APIView):
    # 走一个认证
    authentication_classes = []
    permission_classes = []
    # throttle_classes = []
    # versioning_class = URLPathVersioning
    # parser_classes = []
    def get(self, request, *args, **kwargs):
        print(request.version)
        print(request.user)
        if request.GET:
            print(request.GET)
        return JsonResponse(order_dict)



class TtView(APIView):


    # 走一个认证
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ret = {
            'code':1000,
            'msg':None,
            'token':None
        }
        try:
            # 拿到东西
            user = request._request.POST.get('username')
            pswd = request._request.POST.get('password')
            obj = UserInfo.objects.filter(username=user,password=pswd).first()
            print("yes!")
            # 检测数据库里有没有
            if not obj:
                ret['code'] = 1001
                ret['msg'] = 'error'

            # 生成随机字符串
            else:
                import uuid
                token = uuid.uuid4()
                
                UserToken.objects.update_or_create(user=obj,defaults={'token':token})
                ret['token'] = token
                print(token)
        except Exception as e:
            pass


        return JsonResponse(ret)

from rest_framework import serializers

# class UserInfoSerializer(serializers.Serializer):
        # '''
        # 这里是声明序列化类,都是models.py已有的字段
        # 如果要参与序列化,这里的字段名字一定要和models.py里面的属性同名,如果不参与序列化,就不要在这里声明字段
        # '''

        # # 要取得choice中的数值 user_type_choices
        # user_type = serializers.CharField()

        # # 此方法可以实现基于source参数链表操作
        # get_user_type_display = serializers.CharField()
        # # xxx = serializers.CharField(source="get_user_type_display")
        
        # username = serializers.CharField()
        # password = serializers.CharField()

        # # group对象 source group.id 也可以
        # gp = serializers.CharField(source="group.title")
        
        # # many to many source不大顶 得用自定义显示
        # rls = serializers.SerializerMethodField()
        # # row是当前行的对象
        # def get_rls(self,row):
        #     rls1 = row.roles.all()
        #     ret = []
        #     for item in rls1:
        #         ret.append()
        #     return ret

class UserInfoSerializer(serializers.ModelSerializer):
        
    # 可以自定义字段 也可以自定义方法\
    class Meta:
        
        model = models.UserInfo   # models类名
        # 方法一：生成所有数据库字段
        fields = "__all__"
        depth = 1
        # 方法二：自定义字段名
        # fields = ['username', 'id', 'password','group']
        # depth = 0
        # extra_kwargs ={'group':{source:'group.title'}}



class ModelUserSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required':'不能为空'})
    

import json
class SerView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        # 方法1
        # roles = Role.objects.all().values()
        # roles = list(roles)
        # ret = json.dumps(roles,ensure_ascii=False)
        # return HttpResponse(ret)

        # 方法2
        info = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=info,many=True)

        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)
    
    def post(self, request, *args, **kwargs):

        # 验证，对请求发来的数据进行验证
        ser = ModelUserSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)

        return HttpResponse('POST请求，响应内容')

from .utils.serializers import PagerSerialiser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class MyPageNumberPagination(PageNumberPagination):

    # 默认一页显示3个
    page_size = 3
    # 获取URL参数中传入的页码key字段
    page_query_param = 'page'
    # 指定单页最大值的字段
    page_size_query_param = 'size'
    # 设置单次取的最大值
    max_page_size = 15


class PageView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        # 方法1
        # roles = Role.objects.all().values()
        # roles = list(roles)
        # ret = json.dumps(roles,ensure_ascii=False)
        # return HttpResponse(ret)

        # 方法2
        info = models.Role.objects.all()
        
        # 分页对象
        pg = MyPageNumberPagination()
        pgl = pg.paginate_queryset(queryset=info,request=request,view=self)
        ser = PagerSerialiser(instance=pgl,many=True)

        
        # return Response(ser.data) 
        return pg.get_paginated_response(ser.data)