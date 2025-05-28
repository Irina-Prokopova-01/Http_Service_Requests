from rest_framework import serializers
from shorturl.models import URLrequest


class URLrequestSerializer(serializers.ModelSerializer):
    """
    Serializer for work with URLrequest.
    Used to convert data to and from JSON format.
    """

    class Meta:
        model = URLrequest
        fields = "__all__"

