from django.contrib.gis import admin

from django.contrib.gis.admin import OSMGeoAdmin

from .models import Location

@admin.register(Location)
class ShopAdmin(OSMGeoAdmin):
    list_display = ('point', 'created_by', 'created_at')

