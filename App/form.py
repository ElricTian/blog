
# 用户自定义表单
from django import forms


class RegisterForm(forms.Form):
    # 用户名最少三个字符 required(html5输入框,必选项)
    username = forms.CharField(min_length=3, required=True, error_messages={
        'required': '用户名必须输入',
        'min_length': '用户名至少3个字符'
    })
    password = forms.CharField(min_length=3, required=True, error_messages={
        'required': '密码名必须输入'
        'min_length' '密码至少为6位'
    })
