from django import forms


class MyForm(forms.Form):
    """登录表单验证"""
    user_text = forms.CharField(required=True)