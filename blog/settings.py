import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j+=8k%)i-4+(m(#(4$+hg8ntps38)rxr4-!05i!r3w43yfd!ui'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        # 'PASSWORD': 'charleW@123'
        'PASSWORD': '123456',
        'PORT': 3306,
        # 'HOST': '120.55.40.14'
        'HOST': '127.0.0.1',
    }
}
# 允许嵌入iframe页面 ****
X_FRAME_OPTIONS = 'ALLOWALL'

# XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 遇到的一些问题
# iframe嵌入不允许访问 已解决 iframe scr=/目标视图/  settings加入 X_FRAME_OPTIONS = 'ALLOWALL'
# iframe中 css失效,不小心删掉了 html5 声明
# 生成验证码 如果将验证码渲染到登录界面 提交表单验证码会改变导致输入验证码和原验证码对不上,
# 这里将验证码图片存入缓存,在将验证码存入session中

# 报错'set' object is not reversible  urls.py 里的 {}改成 []
# iframe 跳转只跳转子页面不跳转整个页面 需要使用js跳转 详细查看change_password
# 后端渲染js中的弹窗提示信息 点击第二次才出现上一次的值(异步问题需要ajax解决)
# bug当有重复文章的时候title不是唯一标识 导致查询出错 需要吧id放在网页中(已修改)
# 返回列表功能 js失效(未解决)
# 设置cookie信息看不到过期时间,浏览器问题
