from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [i.name for i in User._meta.fields if i !='id']
 #   list_editable = [i.name for i in User._meta.fields if i !='id']

admin.site.register(User, UserAdmin)