# Generated by Django 4.1.3 on 2022-12-24 09:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_box_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='img/default.png', upload_to='img/', verbose_name='头像'),
        ),
        migrations.CreateModel(
            name='Fold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='img/default2.jpg', upload_to='img/')),
                ('fold_name', models.CharField(default='收藏夹', max_length=64, verbose_name='收藏夹名称')),
                ('box_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.box')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user', to_field='fake_name')),
            ],
        ),
    ]
