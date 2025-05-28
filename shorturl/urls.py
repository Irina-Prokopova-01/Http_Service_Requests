from django.urls import path
from shorturl.views import URLrequestCreateView, URLrequestRetrieveView
from .apps import ShorturlConfig

app_name = ShorturlConfig.name

urlpatterns = [
    path("urls/", URLrequestCreateView.as_view(), name="url-create"),
    path("urls/<str:short_id>/", URLrequestRetrieveView.as_view(), name="url-retrieve"),
    # path("async-request/", UnshortenUrlView.as_view(), name="async_request_example"),
    # path("async-req/", AsyncView.as_view(), name="async_req"),
]



