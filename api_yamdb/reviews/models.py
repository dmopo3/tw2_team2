from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


# class Role(models.TextChoices):
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
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=True)
    bio = models.CharField(max_length=9999)
    role = models.CharField(max_length=99, choices=roles, default=roles[0])


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

    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MinValueValidator(1, 'Минимальное значение 1'),
            MaxValueValidator(10, 'максимальное значение 10'),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Коментарии к отзывам"""

    review = models.ForeignKey(
        Reviews,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,  # Михаил описывает эту модель
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text
