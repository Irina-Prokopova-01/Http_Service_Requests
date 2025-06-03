import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from httpx import AsyncClient
from users.models import CustomUser
from shorturl.models import URLrequest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(email="test@example.com", password="12345")


@pytest.mark.django_db
def test_create_url_request(api_client, user):
    """
    Tests creating a short link with a valid URL
    """
    api_client.force_authenticate(user=user)

    url_data = {"original_url": "http://example.com"}
    response = api_client.post(reverse("shorturl:url-create"), url_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "short_id" in response.data
    assert URLrequest.objects.filter(original_url="http://example.com").exists()


@pytest.mark.django_db
def test_create_url_request_without_url(api_client, user):
    """Tests creating a short link without URL"""
    api_client.force_authenticate(user=user)

    response = api_client.post(reverse("shorturl:url-create"), {})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "URL is required"


@pytest.mark.django_db
def test_retrieve_url_request(api_client, user):
    """Tests getting the original URL by short id"""
    api_client.force_authenticate(user=user)

    url_instance = URLrequest.objects.create(
        original_url="http://example.com", short_id="abc123"
    )

    response = api_client.get(
        reverse("shorturl:url-retrieve", kwargs={"short_id": url_instance.short_id})
    )

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response["Location"] == url_instance.original_url


@pytest.mark.django_db
def test_retrieve_nonexistent_url_request(api_client, user):
    """Tests attempt to get original URL by non-existent short id"""
    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse("shorturl:url-retrieve", kwargs={"short_id": "nonexistent"})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"].code == "not_found"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_fetch_data_from_url(live_server):
    """Tests retrieving data from an external URL. Sends an asynchronous POST request to an endpoint to retrieve data"""
    url_data = {"url": "http://httpbin.org/get"}

    async with AsyncClient(base_url=live_server.url) as client:
        response = await client.post("/shorturl/fetch-data/", json=url_data)

    assert response.status_code == 200
    assert "url" in response.json()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_fetch_data_from_url_without_target(live_server):
    """Tests an attempt to retrieve data without specifying a target URL"""
    async with AsyncClient(base_url=live_server.url) as client:
        response = await client.post("/shorturl/fetch-data/", json={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.decode() == "URL is required"


# @pytest.mark.asyncio
# async def test_fetch_data_from_url():
#     url_data = {"url": "http://httpbin.org/get"}  # Пример использования httpbin для тестирования
#
#     async with AsyncClient() as client:
#         response = await client.post(reverse('shorturl:fetch-data'), json=url_data)
#
#     assert response.status_code == status.HTTP_200_OK
#     assert 'url' in response.json()  # Проверяем, что ответ содержит ожидаемые данные
#
#
# @pytest.mark.asyncio
# async def test_fetch_data_from_url_without_target(api_client):
#     response = await api_client.post(reverse('shorturl:fetch-data'), data={}, format='json')
#
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response.content.decode() == "URL is required"
