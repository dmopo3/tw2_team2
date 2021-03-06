# Generated by Django 2.2.16 on 2022-04-09 06:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ['id'], 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='reviews',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение 1'), django.core.validators.MaxValueValidator(10, 'максимальное значение 10')], verbose_name='Оценка'),
        ),
    ]
