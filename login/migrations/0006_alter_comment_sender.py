# Generated by Django 4.1.2 on 2022-10-31 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_box_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user', to_field='fake_name'),
        ),
    ]
