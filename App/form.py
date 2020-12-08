
# 用户自定义表单
from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    # 用户名最少三个字符 required(html5输入框,必选项)
    username = forms.CharField(min_length=3, required=True, error_messages={
        'required': '用户名必须输入',
        'min_length': '用户名至少3个字符'
    })
    password = forms.CharField(min_length=6, required=True, error_messages={
        'required': '密码名必须输入',
        'min_length': '密码至少为6位'
    })
    confirm = forms.CharField(min_length=6, required=True, error_messages={
        'required': '请再次输入密码',
        'min_length': '密码至少为6位'
    })


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True, error_messages={
        'required': '原密码不能为空!',
    })
    new_password = forms.CharField(min_length=6, required=True, error_messages={
        'required': '新密码不能为空!',
        'min_length': '新密码长度不足!'
    })
    new_password2 = forms.CharField(min_length=6, required=True, error_messages={
        'required': '第二次输入的密码不能为空!',
        'min_length': '新密码长度不足!'
    })

    # 单个字段验证
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password and new_password.isdigit():
            raise ValidationError('密码不能是纯数字!')
        return new_password

    # 全局验证
    def clean(self):
        # 这里使用get方法获取字典中的值,第二个参数为默认值
        # 如果使用dict[],没有当前值则会报错
        new_password = self.cleaned_data.get('new_password', None)
        new_password2 = self.cleaned_data.get('new_password2', '')
        if new_password != new_password2:
            raise ValidationError({'new_password': '两次密码输入不一样!'})
        return self.cleaned_data


