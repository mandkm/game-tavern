from django.db import models
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="locations"
    )

    def __str__(self):
        return self.name