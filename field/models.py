from django.contrib.gis.db import models
from django.conf import settings

class Location(models.Model):
    """
    A model which holds information about a particular location of field
    """
    point = models.GeometryField()
    description = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="locations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]