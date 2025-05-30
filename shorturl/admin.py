from django.contrib import admin

from shorturl.models import URLrequest


@admin.register(URLrequest)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for the User model.
    This class defines which fields will be displayed in the list of users
    in the Django admin panel.
    """

    list_display = ("short_id", "original_url")
