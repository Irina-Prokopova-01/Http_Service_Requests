import aiohttp
import hashlib
import random
import json
from django.http import HttpResponse
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from shorturl.models import URLrequest
from .serializers import URLrequestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny


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


@method_decorator(csrf_exempt, name='dispatch')  # Отключаем аутентификацию
class FetchDataFromURLView(View):
    """Sending async service request and return the data """
    async def post(self, request):
        try:
            data = json.loads(request.body)
            target_url = data.get("url")

            if not target_url:
                return HttpResponse("URL is required", status=400)

            async with aiohttp.ClientSession() as session:
                async with session.get(target_url) as response:
                    # Получаем контент и заголовки от запрашиваемого сайта
                    content = await response.read()
                    content_type = response.headers.get('Content-Type', 'text/html')

                    # Возвращаем ответ "как есть"
                    return HttpResponse(
                        content,
                        status=response.status,
                        content_type=content_type,
                    )

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)