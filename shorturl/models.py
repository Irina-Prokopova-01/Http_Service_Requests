from django.db import models


class URLrequest(models.Model):
    """Model url."""
    original_url = models.URLField(unique=True)
    short_id = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.short_id

    class Meta:
        verbose_name = "url"
        verbose_name_plural = "urls"
