from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser


#class Role(models.TextChoices):
#    """Права доступа для пользователей."""
#    USER = 'user'
#    MODERATOR = 'moderator'
#    ADMIN = 'admin'

    


class User(AbstractUser):
    """Модель пользователя."""
    id = None
    roles = (
        ('USER', 'user'),
        ('MODERATOR', 'moderator'),
        ('ADMIN', 'adminstrator'),
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=True
    )
    bio = models.CharField(max_length=9999)
    role = models.CharField(
        max_length=99,
        choices=roles,
        default=roles[0]
    )


class Categories(models.Model):
    """Категории произведений (Фильмы, книги и тд)."""
    pass


class Genres(models.Model):
    """Жанры произведений"""
    pass


class Titles(models.Model):
    """Произведения"""
    pass


class Reviews(models.Model):
    """Отзывы на произведения"""
    pass


class Comments(models.Model):
    """Коментарии к отзывам"""
    pass
