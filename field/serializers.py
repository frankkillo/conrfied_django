from rest_framework_gis.serializers import GeoFeatureModelSerializer

from field.models import Location


class LocationSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    
    class Meta:
        model = Location
        geo_field = "point"
        fields = ("id", "description", "created_at")
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        instance = super().create(validated_data)
        return instance