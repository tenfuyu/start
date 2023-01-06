# Generated by Django 4.1.3 on 2022-12-25 04:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_box_photo_box_school_user_email_alter_user_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fold',
            name='fold_id',
            field=models.IntegerField(default=1, unique=True, verbose_name='收藏夹序列号'),
            preserve_default=False,
        ),
    ]