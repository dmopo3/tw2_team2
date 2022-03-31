from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.TextChoices):
    """Права доступа для пользователей."""
    pass


class User(AbstractUser):
    """Модель пользователя."""
    pass


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
