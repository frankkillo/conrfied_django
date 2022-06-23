from django.conf import settings

from sentinel.client import get_ndvi

def get_client_from_settings(coords):
    return get_ndvi(settings.SENTINEL_USER, settings.SENTINEL_PASSWORD, coords)