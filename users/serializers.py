from rest_framework.serializers import ModelSerializer

from users.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    """
    Сериализатор пользователя
    """

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password")
