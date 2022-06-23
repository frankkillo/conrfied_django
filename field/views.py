from rest_framework import viewsets, status, authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import Location
from .serializers import LocationSerializer
from .permissions import AuthorModify, IsAdminUserForObject

from sentinel.django_client import get_client_from_settings


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModify | IsAdminUserForObject]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        return self.queryset.filter(created_by=self.request.user)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication])
@permission_classes([AuthorModify|IsAdminUserForObject])
def get_ndvi(request, pk):
    #ADD CELERY WORKER
    location = get_object_or_404(Location, pk=pk)
    data = LocationSerializer(location).data
    del data["id"]
    ndvi_filename = get_client_from_settings(data)

    if not ndvi_filename:
        return Response(data={"detail": "No products available, please try again later"}, status=status.HTTP_204_NO_CONTENT)

    ndvi_img = open(ndvi_filename, 'rb')

    response = FileResponse(ndvi_img)

    return response