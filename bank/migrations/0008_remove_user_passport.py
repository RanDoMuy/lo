# Generated by Django 5.0.6 on 2024-07-06 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_user_passwd_alter_user_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='passport',
        ),
    ]