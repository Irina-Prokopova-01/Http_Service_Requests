import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    """Test to check if user is created with valid data."""
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.check_password("password123")  # Проверка пароля
    assert User.objects.count() == 1  # Проверка, что пользователь создан


@pytest.mark.django_db
def test_create_user_without_email():
    """Test to check user creation without specifying email."""
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="password123")


@pytest.mark.django_db
def test_create_user_with_existing_email():
    """Test to check if a user is created with an existing email."""
    User.objects.create_user(email="test@example.com", password="password123")

    with pytest.raises(Exception):
        User.objects.create_user(email="test@example.com", password="newpassword123")


@pytest.mark.django_db
def test_str_method():
    """Test to check the __str__ method of a custom model."""
    user = User.objects.create_user(email="test@example.com", password="password123")

    assert str(user) == "test@example.com"
