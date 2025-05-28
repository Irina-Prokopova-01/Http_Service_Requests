from django.contrib import admin

from shorturl.models import URLrequest


@admin.register(URLrequest)
class UserAdmin(admin.ModelAdmin):
    """
    Админ. интерфейс для модели User.
    Этот класс определяет, какие поля будут отображаться в списке пользователей
    в административной панели Django.
    """

    list_display = ("short_id", "original_url")
