import datetime
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from App.models import Python, Java, Web, Db, Game, Mobile, User
from utils import bilibili_spider, to_hmac, generate_pin, csdn_spider


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

    if request.method == 'POST':

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if len(old_password) and len(new_password) and len(new_password2) > 0:

            username = request.session.get('username')
            user_info = User.objects.filter(username=username)
            cipher = to_hmac.encryption(old_password)

            if user_info[0].password == cipher:
                if new_password == new_password2:
                    user = User.objects.get(uid=user_info[0].uid)
                    new_cipher = to_hmac.encryption(new_password)
                    user.password = new_cipher
                    user.save()
                    error_message = '修改成功,请重新登录'
                    href = """<html><body onLoad="window.top.location.href='/logout'"></body></html>"""
                    return HttpResponse(href)

                else:
                    error_message = '两次输入的新密码不相同!'
            else:
                error_message = '请输入正确的旧密码!'
        else:
            error_message = '请勿为空!'

    return render(request, 'change_psw.html', locals())


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
    if request.method == 'POST':
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
        href = """<html><body onLoad="window.top.location.href='/'"></body></html>"""
        return HttpResponse(href)

    return render(request, '技术分享/release.html')


def python(request):
    all_article = Python.objects.all().order_by('-release_time')
    count_article = Python.objects.count()

    if request.method == 'POST':
        search = request.POST.get('search_article')
        delete_article_title = request.POST.get('delete_article')
        give_like = request.POST.get('give_like')
        modify_id = request.POST.get('modify')

        if search:
            # 搜索
            all_article = Python.objects.filter(title__icontains=search)

        if delete_article_title:
            # 删除
            try:
                article = Python.objects.get(id=delete_article_title)
                if article:
                    article.delete()
            except Exception as e:
                print(e)

        if give_like:
            # 点赞
            article = Python.objects.get(id=give_like)
            article.like += 1
            article.save()

        if modify_id:
            request.session['id'] = modify_id
            request.session['columns'] = 'python'
            return redirect('/modify/')

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


# 增加数据
def add_data(request):

    all_data = csdn_spider.get_json()

    for data in all_data:
        if ('java'or'Java') in data['title']:
            Java.objects.create(**data)

        else:
            Python.objects.create(**data)

    return HttpResponse('成功')


def modify(request):
    article_id = request.session['id']
    columns = request.session['columns']

    if columns == 'python':
        article = Python.objects.get(id=article_id)
    elif columns == 'java':
        article = Java.objects.get(id=article_id)
    elif columns == 'db':
        article = Db.objects.get(id=article_id)
    elif columns == 'game':
        article = Game.objects.get(id=article_id)
    elif columns == 'mobile':
        article = Mobile.objects.get(id=article_id)
    elif columns == 'web':
        article = Web.objects.get(id=article_id)

    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        url = request.POST.get('url')
        data = {'author': author, 'title': title, 'url': url}

        if columns == 'python':
            article = Python.objects.filter(id=article_id).update(**data)
        elif columns == 'java':
            article = Java.objects.filter(id=article_id).update(**data)
        elif columns == 'db':
            article = Db.objects.filter(id=article_id).update(**data)
        elif columns == 'game':
            article = Game.objects.filter(id=article_id).update(**data)
        elif columns == 'mobile':
            article = Mobile.objects.filter(id=article_id).update(**data)
        elif columns == 'web':
            article = Web.objects.filter(id=article_id).update(**data)
        href = """<html><body onLoad="window.top.location.href='/'"></body></html>"""
        return HttpResponse(href)

    return render(request, '技术分享/modify.html', locals())
