import hashlib
import random
import httpx
from rest_framework.generics import GenericAPIView
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from shorturl.models import URLrequest
from .serializers import URLrequestSerializer
from rest_framework.permissions import IsAuthenticated


class URLrequestCreateView(generics.CreateAPIView):
    """
    Creating object short url
    """
    serializer_class = URLrequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        original_url = request.data.get("original_url")
        if not original_url:
            raise ValidationError({'error': 'URL is required'})

        existing_url = URLrequest.objects.filter(original_url=original_url).first()
        if existing_url:
            return Response({'short_id': f"{self.get_base_url()}/{existing_url.short_id}"}, status=status.HTTP_200_OK)

        short_id = self.generate_short_id(original_url)

        url_instance = URLrequest(original_url=original_url, short_id=short_id)
        url_instance.save()

        return Response({'short_id': f"{self.get_base_url()}/{short_id}"}, status=status.HTTP_201_CREATED)

    def get_base_url(self):
        return f"http://{self.request.get_host()}"

    def generate_short_id(self, original_url):
        short_id = hashlib.md5(original_url.encode()).hexdigest()[:6]
        while URLrequest.objects.filter(short_id=short_id).exists():
            short_id = hashlib.md5((original_url + str(random.random())).encode()).hexdigest()[:6]
        return short_id


class URLrequestRetrieveView(generics.RetrieveAPIView):
    """
    Retrieving object short url
    """
    serializer_class = URLrequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = URLrequest.objects.all()
    lookup_field = 'short_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            return Response(status=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": instance.original_url})
            # return super().retrieve(request, *args, **kwargs)
        except URLrequest.DoesNotExist:
            return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
import asyncio
async def async_request_example(request):
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000/shorturl/urls/')
        return Response(response.json(), status=response.status_code)

#
# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import ValidationError
# from asgiref.sync import sync_to_async
# from .models import URLrequest
# from .serializers import URLrequestSerializer
# import hashlib
# from asgiref.sync import sync_to_async
# import random
#
#
# class URLrequestCreateView(APIView):
#     """
#     Async view for creating short URLs
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = URLrequestSerializer
#
#     async def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         original_url = request.data.get("original_url")
#         if not original_url:
#             raise ValidationError({'error': 'URL is required'})
#
#         # Async ORM queries
#         existing_url = await sync_to_async (URLrequest.objects.filter(original_url=original_url).afirst)()
#         if existing_url:
#             return Response(
#                 {'short_id': f"{await self.get_base_url()}/{existing_url.short_id}"},
#                 status=status.HTTP_200_OK
#             )
#
#         short_id = await self.generate_short_id(original_url)
#
#         # Async save
#         url_instance = URLrequest(
#             original_url=original_url,
#             short_id=short_id,
#             user=request.user  # Assuming you want to associate with user
#         )
#         await sync_to_async(url_instance.save)()
#
#         return Response(
#             {'short_id': f"{await self.get_base_url()}/{short_id}"},
#             status=status.HTTP_201_CREATED
#         )
#
#     async def get_base_url(self):
#         return f"http://{self.request.get_host()}"
#
#     async def generate_short_id(self, original_url):
#         short_id = hashlib.md5(original_url.encode()).hexdigest()[:6]
#         while await URLrequest.objects.filter(short_id=short_id).aexists():
#             short_id = hashlib.md5((original_url + str(random.random())).encode()).hexdigest()[:6]
#         return short_id
#
#
# class URLrequestRetrieveView(generics.RetrieveAPIView):
#     """
#     Retrieving object short url
#     """
#     serializer_class = URLrequestSerializer
#     permission_classes = [IsAuthenticated]
#     # queryset = URLrequest.objects.all()
#     lookup_field = 'short_id'
#
#     async def get(self, request, *args, **kwargs):
#         try:
#             instance = await sync_to_async(self.get_object)()
#             return Response(status=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": instance.original_url})
#             # return super().retrieve(request, *args, **kwargs)
#         except URLrequest.DoesNotExist:
#             return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def get_object(self):
#         # Здесь должен быть код для получения объекта по short_id
#         # Например:
#         return URLrequest.objects.get(short_id=self.kwargs['short_id'])
