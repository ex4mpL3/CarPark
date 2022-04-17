from rest_framework.serializers import ModelSerializer

from driver.serializers import DriversSerializer
from vehicle.models import Vehicle


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'plate_number', 'driver_id', 'make']


class GetVehicleSerializer(VehicleSerializer):
    driver_id = DriversSerializer(read_only=True, many=False)
