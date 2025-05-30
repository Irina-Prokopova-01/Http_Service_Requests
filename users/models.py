from django.contrib.auth.models import AbstractUser
from django.db import models
from users.services import UserManager


class CustomUser(AbstractUser):
    """
    Model user
    """

    username = None
    email = models.EmailField(unique=True, help_text="Enter your email")
    first_name = models.CharField(max_length=30, help_text="Please enter your name")
    last_name = models.CharField(max_length=30, help_text="Please enter your last name")
    phone = models.CharField(
        max_length=20,
        verbose_name="Phone number",
        blank=True,
        null=True,
        help_text="Enter phone number",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("email",)
