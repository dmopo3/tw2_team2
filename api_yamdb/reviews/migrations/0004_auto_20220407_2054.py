# Generated by Django 2.2.16 on 2022-04-07 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220407_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=99),
        ),
    ]
