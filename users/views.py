from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserCreateAPIView(CreateAPIView):
    """User creation controller."""

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Change the logic of the controller to properly register the user."""

        # Сохраняю пользователя и сразу делаю его активным
        user = serializer.save(is_active=True)
        # Хэширую пароль пользователя и сохраняю пользователя
        user.set_password(user.password)
        user.save()