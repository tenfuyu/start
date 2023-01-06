from django.forms import ModelForm
from django import forms
from login import models
from ckeditor.fields import RichTextFormField


# modelform配合instance
class BoxForm(forms.Form):
    school=forms.CharField(label='高校',widget=forms.TextInput)
    real_name = forms.CharField(label='姓名', widget=forms.TextInput)
    gender = forms.ChoiceField(label='性别', choices=((1, '男'), (2, '女')))
    age = forms.IntegerField(label='年龄', widget=forms.TextInput,required=False)
    area = forms.CharField(label='地区', widget=forms.TextInput, required=False)
    phone = forms.CharField(label='电话', widget=forms.TextInput, required=False)
    info = forms.CharField(label='个人信息', widget=forms.TextInput, required=False)
    free= RichTextFormField(label='内容')


class UserForm(forms.Form):
    fake_name = forms.CharField(label='昵称', widget=forms.TextInput)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)


class RegisterForm(ModelForm):
    class Meta:
        model = models.User
        fields = ['fake_name', 'password','email']


class FindForm(forms.Form):
    email = forms.EmailField(label='邮箱',widget=forms.EmailInput)


class RePassword(forms.Form):
    re_password = forms.CharField(label='新密码',widget=forms.PasswordInput)


class CommentForm(forms.Form):
    content = forms.CharField(label='请输入你的评论：', widget=forms.TextInput)


class Name(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['fake_name']


class Com2Form(forms.Form):
    content = forms.CharField(label='回复', widget=forms.TextInput)