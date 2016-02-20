from rest_framework.serializers import ModelSerializer
from backend.models import SoftwareConfiguration


class SoftwareConfigurationSerializer(ModelSerializer):
    class Meta:
        model = SoftwareConfiguration
        exclude = ()
