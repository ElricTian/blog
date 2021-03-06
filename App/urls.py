from django.urls import path, re_path
from django.views.generic import RedirectView
from App import views

urlpatterns = [
    # 网站图标
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')),

    # 登录
    path('login/', views.login, name='login'),
    # 验证码图片
    path('pin_img/', views.pin_img, name='pin_img'),
    # 登出
    path('logout/', views.logout, name='logout'),
    # 修改密码
    path('change_psw/', views.change_password, name='change_psw'),

    # 主页
    path('', views.index, name='index'),
    # 主页左边导航栏
    path('index_left/', views.index_left, name='index_left'),
    # 标题栏
    path('index_head/', views.index_head, name='index_header'),

    # 超级管理员主页
    path('super_index/', views.super_index, name='super_index'),
    # 超级管理员左边导航栏
    path('super_left/', views.super_left, name='super_left'),
    path('super_label/', views.super_label, name='super_label'),
    # 超级管理员选项卡
    path('super_list/', views.super_list, name='super_list'),


    # 技术分享
    path('modify/', views.modify, name='modify'),
    path('release/', views.release, name='release'),
    path('python/<int:page>', views.python, name='python'),
    path('java/<int:page>', views.java, name='java'),
    path('web/<int:page>', views.web, name='web'),
    path('db/<int:page>', views.db, name='db'),
    path('game/<int:page>', views.game, name='game'),
    path('mobile/<int:page>', views.mobile, name='mobile'),


    # path('manage/', views.manage, name='manage'),


    # 随机视频
    path('video/', views.video, name='video'),

    # 照片
    path('picture_content/', views.photos, name='photos'),
    # 相册
    path('picture_management/', views.album, name='album'),

    # 留言板
    path('message_broad/', views.message_broad, name='message_broad'),

    # 修改资料
    path('system_set/', views.system_set, name='system_set'),

    # 增加数据
    path('add_data/', views.add_data, name='add_data'),

    # django form表单验证 以及用户认证
    path('register', views.register, name='register')
]
