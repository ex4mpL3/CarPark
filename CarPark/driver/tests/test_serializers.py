from django.test import TestCase

from driver.models import Driver
from driver.serializers import DriversSerializer


class DriversSerializerTestCase(TestCase):
    def test_ok(self):
        driver1 = Driver.objects.create(first_name='Ruslan', last_name='Yarovoy')
        data = DriversSerializer(driver1).data
        expected_data = {
            'id': driver1.id,
            'first_name': 'Ruslan',
            'last_name': 'Yarovoy'
        }
        self.assertEqual(expected_data, data)
