# Generated by Django 5.0.6 on 2024-06-25 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_rename_date_of_birth_user_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reward_balance',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999999999)], verbose_name='Reward Balance'),
        ),
    ]
