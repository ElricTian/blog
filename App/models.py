from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


# 自定义管理器
class MyManager(Manager):

    def get_queryset(self):
        data = super().get_queryset().filter(like=0)
        return data


class Python(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    release_time = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=255)
    like = models.IntegerField(blank=True, null=False, default=0)
    # python_manage = MyManager()

    class Meta:
        managed = False
        db_table = 'python'


class Java(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    release_time = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=255)
    like = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'java'


class Game(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    release_time = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=255)
    like = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'game'


class Mobile(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    release_time = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=255)
    like = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'mobile'


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    # 注册时间自动创建
    regtime = models.DateTimeField(auto_now_add=True)

    # 自定义一个新的管理器,名字为new_manage
    # new_manage = Manager()

    class Meta:
        managed = False
        db_table = 'user'


class Web(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    release_time = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=255)
    like = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'web'


class Db(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    release_time = models.DateTimeField(blank=False, null=False)
    url = models.CharField(max_length=255)
    like = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'db'


class NewUser(AbstractUser):
    class Meta:
        managed = True
        db_table = 'new_user'

