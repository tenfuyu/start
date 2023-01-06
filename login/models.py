import django.utils.timezone as timezone
from django.db import models
from ckeditor.fields import RichTextField



class User(models.Model):
    fake_name = models.CharField(max_length=32, verbose_name='昵称', unique=True)
    password = models.CharField(max_length=64, verbose_name="密码")
    photo = models.ImageField(default='img/default.png', upload_to='img/',verbose_name='头像')
    email = models.EmailField(unique=True,null=True,verbose_name='邮箱')


class PickHistory(models.Model):
    picker = models.ForeignKey(to='User', to_field='fake_name', on_delete=models.CASCADE)
    box = models.ForeignKey(to='Box', to_field='id', on_delete=models.CASCADE)


class Comment(models.Model):
    sender = models.ForeignKey(to='User', to_field='fake_name', on_delete=models.CASCADE)
    content = models.TextField()
    to_box = models.ForeignKey(to='Box', to_field='id', on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)


class InfComment(models.Model):
    sender = models.ForeignKey(to='User', to_field='fake_name', on_delete=models.CASCADE)
    content = models.TextField()
    to_comment = models.ForeignKey(to='Comment', to_field='id', on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)


class Fold(models.Model):
    img = models.ImageField(default='img/default2.jpg', upload_to='img/')
    box_id=models.ForeignKey(to="Box",to_field='id',on_delete=models.CASCADE)
    creator=models.ForeignKey(to="User",to_field='fake_name',on_delete=models.CASCADE)
    fold_name=models.CharField(max_length=64,verbose_name="收藏夹名称",default='收藏夹')
    fold_id = models.IntegerField(verbose_name='收藏夹序列号')


class Box(models.Model):
    school=models.CharField(max_length=64,null=True,verbose_name="高校")
    sender = models.ForeignKey(to='User', to_field='fake_name', on_delete=models.CASCADE)
    real_name = models.CharField(max_length=32, verbose_name="姓名")
    gender = models.SmallIntegerField(choices=((1, '男'), (2, '女')), verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄",null=True)
    phone = models.CharField(max_length=32, null=True, verbose_name="电话")
    area = models.CharField(max_length=64, null=True, verbose_name="地区")
    info = models.TextField(null=True, default='该用户未设置签名', verbose_name="个性签名")
    time = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(default='img/default_box.png', upload_to='img/',verbose_name='封面')
    free = RichTextField(verbose_name='内容',config_name='default')

