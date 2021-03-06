import datetime
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from App.form import RegisterForm, ChangePasswordForm
from App.models import Python, Java, Web, Db, Game, Mobile, User, NewUser
from utils import bilibili_spider, to_hmac, generate_pin, csdn_spider


# 装饰器,路由保护 建立session时才能访问
def check_login(func):
    def inner(*args, **kwargs):
        if args[0].session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect('login')
    return inner


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

            if user_info[0].password == cipher:
                if pin == check_code:
                    response = redirect('/')
                    # 设置cookie过期时间
                    future = datetime.datetime.now() + datetime.timedelta(days=1)
                    response.set_cookie('username', username, expires=future)
                    # 将用户名加入session
                    request.session['username'] = username

                    return response

                else:
                    message = '验证码错误'
            else:
                message = '密码错误'
        else:
            message = '无此用户'

    return render(request, 'login.html', locals())


@check_login
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


@check_login
def change_password(request):

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data
            old_password = data['old_password']
            new_password = data['new_password']
            new_password2 = data['new_password2']

            # 查询
            username = request.session.get('username')
            user_info = User.objects.filter(username=username)
            # 加密验证
            cipher = to_hmac.encryption(old_password)

            if user_info[0].password == cipher:

                user = User.objects.get(uid=user_info[0].uid)
                new_cipher = to_hmac.encryption(new_password)
                user.password = new_cipher
                user.save()
                error_message = '修改成功,请重新登录'
                href = """<html><body onLoad="window.top.location.href='/logout'"></body></html>"""
                return HttpResponse(href)
            else:
                error_message = '旧密码不正确'
        else:
            # 把错误信息传给前端
            error_message = None
            for value in form.errors.get_json_data().values():
                error_message = value[0]['message']
                break
            return render(request, 'change_psw.html', locals())
    return render(request, 'change_psw.html', locals())


@check_login
def index(request):
    """主页"""
    if not request.session.get('username'):
        return redirect('/login')
    else:
        return render(request, 'index.html')


@check_login
def index_left(request):
    return render(request, 'index_left.html')


@check_login
def index_head(request):
    username = request.session.get('username')
    return render(request, 'index_head.html', locals())


@check_login
def super_index(request):
    """超级模式"""
    return render(request, 'super_index.html')


@check_login
def super_left(request):
    return render(request, 'super_left.html')


@check_login
def super_list(request):
    return render(request, 'super/super_list.html')


@check_login
def super_label(request):
    return render(request, 'super/super_label.html')


@check_login
def release(request):
    """发布文章"""
    select_table = request.POST.get('table')
    author = request.POST.get('author')
    title = request.POST.get('title')
    url = request.POST.get('url')
    release_time = request.POST.get('release_time')
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


@check_login
def python(request, page):

    # 所有数据
    articles = Python.objects.all().order_by('-release_time')
    # 分页
    paginator = Paginator(articles, 10)
    # 共多少页
    count_page = paginator.num_pages
    # 当前页
    now_page = page
    # 每一页
    pager = paginator.page(page)
    all_article = pager.object_list

    if pager.has_previous():
        # 上一页
        previous_page = pager.previous_page_number()
    if pager.has_next():
        # 下一页
        next_page = pager.next_page_number()
        # 下下页
        nnext_page = pager.next_page_number() + 1

    # 统计一共多少篇文章
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
            request.session['columns'] = 'Python'
            return redirect('/modify/')
    return render(request, '技术分享/python.html', locals())


@check_login
def java(request, page):
    # 所有数据
    articles = Java.objects.all().order_by('-release_time')
    # 分页
    paginator = Paginator(articles, 10)
    # 共多少页
    count_page = paginator.num_pages
    # 当前页
    now_page = page
    # 每一页
    pager = paginator.page(page)
    all_article = pager.object_list

    if pager.has_previous():
        # 上一页
        previous_page = pager.previous_page_number()
    if pager.has_next():
        # 下一页
        next_page = pager.next_page_number()
        # 下下页
        nnext_page = pager.next_page_number() + 1

    # 统计一共多少篇文章
    count_article = Java.objects.count()

    if request.method == 'POST':
        search = request.POST.get('search_article')
        delete_article_title = request.POST.get('delete_article')
        give_like = request.POST.get('give_like')
        modify_id = request.POST.get('modify')

        if search:
            # 搜索
            all_article = Java.objects.filter(title__icontains=search)

        if delete_article_title:
            # 删除
            try:
                article = Java.objects.get(id=delete_article_title)
                if article:
                    article.delete()
            except Exception as e:
                print(e)

        if give_like:
            # 点赞
            article = Java.objects.get(id=give_like)
            article.like += 1
            article.save()

        if modify_id:
            request.session['id'] = modify_id
            request.session['columns'] = 'java'
            return redirect('/modify/')
    return render(request, '技术分享/java.html', locals())


@check_login
def web(request, page):
    # 所有数据
    articles = Web.objects.all().order_by('-release_time')
    # 分页
    paginator = Paginator(articles, 10)
    # 共多少页
    count_page = paginator.num_pages
    # 当前页
    now_page = page
    # 每一页
    pager = paginator.page(page)
    all_article = pager.object_list

    if pager.has_previous():
        # 上一页
        previous_page = pager.previous_page_number()
    if pager.has_next():
        # 下一页
        next_page = pager.next_page_number()
        # 下下页
        nnext_page = pager.next_page_number() + 1

    # 统计一共多少篇文章
    count_article = Web.objects.count()

    if request.method == 'POST':
        search = request.POST.get('search_article')
        delete_article_title = request.POST.get('delete_article')
        give_like = request.POST.get('give_like')
        modify_id = request.POST.get('modify')

        if search:
            # 搜索
            all_article = Web.objects.filter(title__icontains=search)

        if delete_article_title:
            # 删除
            try:
                article = Web.objects.get(id=delete_article_title)
                if article:
                    article.delete()
            except Exception as e:
                print(e)

        if give_like:
            # 点赞
            article = Web.objects.get(id=give_like)
            article.like += 1
            article.save()

        if modify_id:
            request.session['id'] = modify_id
            request.session['columns'] = 'web'
            return redirect('/modify/')
    return render(request, '技术分享/web.html', locals())


@check_login
def db(request, page):
    # 所有数据
    articles = Db.objects.all().order_by('-release_time')
    # 分页
    paginator = Paginator(articles, 10)
    # 共多少页
    count_page = paginator.num_pages
    # 当前页
    now_page = page
    # 每一页
    pager = paginator.page(page)
    all_article = pager.object_list

    if pager.has_previous():
        # 上一页
        previous_page = pager.previous_page_number()
    if pager.has_next():
        # 下一页
        next_page = pager.next_page_number()
        # 下下页
        nnext_page = pager.next_page_number() + 1

    # 统计一共多少篇文章
    count_article = Db.objects.count()

    if request.method == 'POST':
        search = request.POST.get('search_article')
        delete_article_title = request.POST.get('delete_article')
        give_like = request.POST.get('give_like')
        modify_id = request.POST.get('modify')

        if search:
            # 搜索
            all_article = Db.objects.filter(title__icontains=search)

        if delete_article_title:
            # 删除
            try:
                article = Db.objects.get(id=delete_article_title)
                if article:
                    article.delete()
            except Exception as e:
                print(e)

        if give_like:
            # 点赞
            article = Db.objects.get(id=give_like)
            article.like += 1
            article.save()

        if modify_id:
            request.session['id'] = modify_id
            request.session['columns'] = 'db'
            return redirect('/modify/')
    return render(request, '技术分享/db.html', locals())


@check_login
def game(request, page):
    # 所有数据
    articles = Game.objects.all().order_by('-release_time')
    # 分页
    paginator = Paginator(articles, 10)
    # 共多少页
    count_page = paginator.num_pages
    # 当前页
    now_page = page
    # 每一页
    pager = paginator.page(page)
    all_article = pager.object_list

    if pager.has_previous():
        # 上一页
        previous_page = pager.previous_page_number()
    if pager.has_next():
        # 下一页
        next_page = pager.next_page_number()
        # 下下页
        nnext_page = pager.next_page_number() + 1

    # 统计一共多少篇文章
    count_article = Game.objects.count()

    if request.method == 'POST':
        search = request.POST.get('search_article')
        delete_article_title = request.POST.get('delete_article')
        give_like = request.POST.get('give_like')
        modify_id = request.POST.get('modify')

        if search:
            # 搜索
            all_article = Game.objects.filter(title__icontains=search)

        if delete_article_title:
            # 删除
            try:
                article = Game.objects.get(id=delete_article_title)
                if article:
                    article.delete()
            except Exception as e:
                print(e)

        if give_like:
            # 点赞
            article = Game.objects.get(id=give_like)
            article.like += 1
            article.save()

        if modify_id:
            request.session['id'] = modify_id
            request.session['columns'] = 'game'
            return redirect('/modify/')
    return render(request, '技术分享/game.html', locals())


@check_login
def mobile(request, page):
    # 所有数据
    articles = Mobile.objects.all().order_by('-release_time')
    # 分页
    paginator = Paginator(articles, 10)
    # 共多少页
    count_page = paginator.num_pages
    # 当前页
    now_page = page
    # 每一页
    pager = paginator.page(page)
    all_article = pager.object_list

    if pager.has_previous():
        # 上一页
        previous_page = pager.previous_page_number()
    if pager.has_next():
        # 下一页
        next_page = pager.next_page_number()
        # 下下页
        nnext_page = pager.next_page_number() + 1

    # 统计一共多少篇文章
    count_article = Mobile.objects.count()

    if request.method == 'POST':
        search = request.POST.get('search_article')
        delete_article_title = request.POST.get('delete_article')
        give_like = request.POST.get('give_like')
        modify_id = request.POST.get('modify')

        if search:
            # 搜索
            all_article = Mobile.objects.filter(title__icontains=search)

        if delete_article_title:
            # 删除
            try:
                article = Mobile.objects.get(id=delete_article_title)
                if article:
                    article.delete()
            except Exception as e:
                print(e)

        if give_like:
            # 点赞
            article = Mobile.objects.get(id=give_like)
            article.like += 1
            article.save()

        if modify_id:
            request.session['id'] = modify_id
            request.session['columns'] = 'mobile'
            return redirect('/modify/')

    return render(request, '技术分享/mobile.html', locals())


@check_login
def video(request):
    """随机视频"""
    aid = bilibili_spider.get_aid()
    return render(request, '视频/video.html', locals())


@check_login
def photos(request):
    """照片"""
    return render(request, 'picture/photos.html')


@check_login
def album(request):
    """相册"""
    return render(request, 'picture/album.html')


@check_login
def message_broad(request):
    """留言板"""
    return render(request, '留言板/zixun_Team.html')


# 系统设置
@check_login
def system_set(request):
    return render(request, 'system_set.html')


# 增加数据
@check_login
def add_data(request):

    all_data = csdn_spider.get_json()

    for data in all_data:
        if ('java'or'Java') in data['title']:
            Java.objects.create(**data)

        else:
            Game.objects.create(**data)

    return HttpResponse('成功')


@check_login
def modify(request):
    """修改文章"""
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


# 测试单元
# def manage(request):
#     data = Python.python_manage.all()
#     print(data)
#     return HttpResponse('OK')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # 进行验证
        if form.is_valid():
            # data是字典
            data = form.cleaned_data
            data.pop('confirm')

            # 把用户写入数据库
            # 这里的密码不能手动加密密码 Django用的是自己的加密方式
            # 创建用户的方法必须是模型的方法
            user = NewUser.objects.create_user(**data)
            if user:
                return HttpResponse('注册成功')
        else:
            # 把错误信息传给前端
            error_message = None
            for value in form.errors.get_json_data().values():
                error_message = value[0]['message']
                break
            return render(request, 'register.html', locals())
    return render(request, 'register.html')
