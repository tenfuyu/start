# Generated by Django 4.1.2 on 2022-11-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_comment_time_pickhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='age',
            field=models.IntegerField(null=True, verbose_name='年龄'),
        ),
    ]
