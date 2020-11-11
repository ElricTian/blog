import datetime
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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


def video(request):
    """随机视频"""
    aid = bilibili_spider.get_aid()
    return render(request, '视频/video.html', locals())


def photos(request):
    """照片"""
    return render(request, 'picture/photos.html')


def album(request):
    """相册"""
    return render(request, 'picture/album.html')


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
            Game.objects.create(**data)

    return HttpResponse('成功')


# 修改数据
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


# 测试单元
def manage(request):
    data = Python.python_manage.all()
    print(data)
    return HttpResponse('OK')
