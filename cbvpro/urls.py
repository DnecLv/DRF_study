from django.urls import path,re_path
from django.conf.urls import url
from . import views

app_name = 'cbvpro'
urlpatterns = [
    path('1/',views.TurView.as_view(), name="main"),
    re_path(r'^(?P<version>[v1|v2]+)/auth/',views.TtView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/info/',views.GetInfo.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/ser/',views.SerView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/role/',views.PageView.as_view()),
]
