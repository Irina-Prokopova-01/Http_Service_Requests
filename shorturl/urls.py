from django.urls import path
from shorturl.views import URLrequestCreateView, URLrequestRetrieveView, FetchDataFromURLView
from .apps import ShorturlConfig

app_name = ShorturlConfig.name

urlpatterns = [
    path("urls/", URLrequestCreateView.as_view(), name="url-create"),
    path("urls/<str:short_id>/", URLrequestRetrieveView.as_view(), name="url-retrieve"),
    path("fetch-data/", FetchDataFromURLView.as_view(), name="fetch-data"),
]


