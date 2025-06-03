from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for the User model.
    This class defines which fields will be displayed in the list of users
    in the Django admin panel
    """

    list_display = ("id", "first_name", "last_name", "email")
