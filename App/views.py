import datetime
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from App.models import Python, Java, Web, Db, Game, Mobile, User
from utils import bilibili_spider, to_hmac, generate_pin


def login(request):
    message = '请注意大小写'

    if request.method == 'POST':

        pin = request.session.get('pin')
        username = request.POST.get('username')
        password = request.POST.get('password')
        check_code = request.POST.get('check_code')
        user_info = User.objects.filter(username=username)

        if user_info:
            cipher = to_hmac.encryption(password)

            # 将用户名加入session
            request.session['username'] = username

            if user_info[0].password == cipher:
                if pin == check_code:
                    return redirect('/')
                else:
                    message = '验证码错误'
            else:
                message = '密码错误'
        else:
            message = '无此用户'

    return render(request, 'login.html', locals())


def logout(request):
    del request.session['username']
    return redirect('/')


def pin_img(request):
    """验证码"""
    img, pin = generate_pin.generation_img()
    f = BytesIO()
    img.save(f, "png")
    request.session['pin'] = pin
    # 从内存中获取并返回给前端
    code_img = f.getvalue()
    return HttpResponse(code_img)


def change_password(request):
    return render(request, 'change_psw.html')


def index(request):
    """主页"""
    if not request.session.get('username'):
        return redirect('/login')
    else:
        return render(request, 'index.html')


def index_left(request):
    return render(request, 'index_left.html')


def index_head(request):
    username = request.session.get('username')
    return render(request, 'index_head.html', locals())


# 超级用户
def super_index(request):
    return render(request, 'super_index.html')


def super_left(request):
    return render(request, 'super_left.html')


def super_list(request):
    return render(request, 'super/super_list.html')


def super_label(request):
    return render(request, 'super/super_label.html')


# 技术分享
def release(request):
    """发布文章"""
    select_table = request.POST.get('table')
    author = request.POST.get('author')
    title = request.POST.get('title')
    url = request.POST.get('url')
    release_time = datetime.datetime.now()
    article = {'author': author, 'title': title, 'url': url, 'release_time': release_time}
    print(article)

    if select_table == 'python':
        Python.objects.create(**article)
    elif select_table == 'java':
        Java.objects.create(**article)
    elif select_table == 'web':
        Web.objects.create(**article)
    elif select_table == 'db':
        Db.objects.create(**article)
    elif select_table == 'game':
        Game.objects.create(**article)
    elif select_table == 'mobile':
        Mobile.objects.create(**article)

    return render(request, '技术分享/release.html')


def python(request):
    all_article = Python.objects.all().order_by('-release_time')
    count_article = Python.objects.count()
    search = request.POST.get('search_article')
    if search:
        all_article = Python.objects.filter(title__icontains=search)
    return render(request, '技术分享/python.html', locals())


def java(request):
    all_article = Java.objects.all().order_by('-release_time')
    count_article = Java.objects.count()
    search = request.POST.get('search_article')
    if search:
        all_article = Java.objects.filter(title__icontains=search)
    return render(request, '技术分享/java.html', locals())


def web(request):
    all_article = Web.objects.all().order_by('-release_time')
    count_article = Web.objects.count()
    search = request.POST.get('search_article')
    if search:
        all_article = Web.objects.filter(title__icontains=search)
    return render(request, '技术分享/web.html', locals())


def db(request):
    all_article = Db.objects.all().order_by('-release_time')
    count_article = Db.objects.count()
    search = request.POST.get('search_article')
    if search:
        all_article = Db.objects.filter(title__icontains=search)
    return render(request, '技术分享/db.html', locals())


def game(request):
    all_article = Game.objects.all().order_by('-release_time')
    count_article = Game.objects.count()
    search = request.POST.get('search_article')
    if search:
        all_article = Game.objects.filter(title__icontains=search)
    return render(request, '技术分享/game.html', locals())


def mobile(request):
    all_article = Mobile.objects.all().order_by('-release_time')
    count_article = Mobile.objects.count()
    search = request.POST.get('search_article')
    if search:
        all_article = Mobile.objects.filter(title__icontains=search)
    return render(request, '技术分享/mobile.html', locals())


def video(request):
    """随机视频"""
    aid = bilibili_spider.get_aid()
    return render(request, '视频/video.html', locals())


def picture_content(request):
    """相册管理"""
    return render(request, 'picture/picture_content.html')


def picture_management(request):
    return render(request, 'picture/picture_management.html')


# 留言板
def message_broad(request):
    return render(request, '留言板/zixun_Team.html')


# 系统设置
def system_set(request):
    return render(request, 'system_set.html')


