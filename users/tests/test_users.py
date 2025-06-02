import pytest
from users.models import CustomUser


@pytest.mark.django_db
def test_create_user():
    """Test to check if user is created with valid data."""
    user = CustomUser.objects.create_user(
        email="test@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.check_password("password123")  # Проверка пароля
    assert CustomUser.objects.count() == 1  # Проверка, что пользователь создан


@pytest.mark.django_db
def test_create_user_without_email():
    """Test to check user creation without specifying email."""
    with pytest.raises(ValueError):
        CustomUser.objects.create_user(email="", password="password123")


@pytest.mark.django_db
def test_create_user_with_existing_email():
    """Test to check if a user is created with an existing email."""
    CustomUser.objects.create_user(email="test@example.com", password="password123")

    with pytest.raises(Exception):
        CustomUser.objects.create_user(email="test@example.com", password="newpassword123")


@pytest.mark.django_db
def test_str_method():
    """Test to check the __str__ method of a custom model."""
    user = CustomUser.objects.create_user(email="test@example.com", password="password123")

    assert str(user) == "test@example.com"
