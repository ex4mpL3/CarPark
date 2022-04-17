from rest_framework.serializers import ModelSerializer

from .models import Driver


class DriversSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name']
