# Generated by Django 5.1.3 on 2024-11-12 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_is_active_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
    ]
