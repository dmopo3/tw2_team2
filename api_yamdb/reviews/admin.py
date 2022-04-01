from django.contrib import admin

from .models import Comments, Reviews, User


class UserAdmin(admin.ModelAdmin):
    list_display = [i.name for i in User._meta.fields if i != 'id']


#   list_editable = [i.name for i in User._meta.fields if i !='id']


class ReviewsAdmin(admin.ModelAdmin):
    """Класс для отображения полей отзыва в админке."""

    list_display = (
        'pk',
        'text',
        'author',
        'score',
        'pub_date',
        'title',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    """Класс для отображения полей комментария в админке."""

    list_display = (
        'pk',
        'text',
        'author',
        'pub_date',
        'review',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comments, CommentsAdmin)
