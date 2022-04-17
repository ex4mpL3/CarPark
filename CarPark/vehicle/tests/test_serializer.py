from django.test import TestCase

from driver.models import Driver
from driver.serializers import DriversSerializer
from vehicle.models import Vehicle
from vehicle.serializers import GetVehicleSerializer


class VehiclesSerializerTestCase(TestCase):
    def test_ok(self):
        driver1 = Driver.objects.create(first_name='Ruslan', last_name='Yarovoy')
        vehicle1 = Vehicle.objects.create(
            driver_id=driver1,
            make='1999',
            plate_number='AE 7777 AK',
            model='BMW'
        )
        data = GetVehicleSerializer(vehicle1).data
        expected_data = {
            'id': vehicle1.id,
            'driver_id': DriversSerializer(driver1).data,
            'make': '1999',
            'plate_number': 'AE 7777 AK',
            'model': 'BMW'
        }
        self.assertEqual(expected_data, data)
