from django.urls import path

from .views import LocationViewSet, get_ndvi

loc_list = LocationViewSet.as_view({"get": "list", "post": "create"})
loc_del = LocationViewSet.as_view({"get": "retrieve", "delete": "destroy"})

urlpatterns = [
    path('locations/', loc_list, name="location_list"),
    path('locations/<int:pk>/', loc_del, name="location_delete"),
    path('locations/<int:pk>/ndvi/', get_ndvi, name="get_ndvi")
]