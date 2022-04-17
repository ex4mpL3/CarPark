import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from driver.models import Driver
from vehicle.models import Vehicle
from vehicle.serializers import GetVehicleSerializer


class VehicleApiTestCase(APITestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(first_name='Ruslan', last_name='Yarovoy')
        self.vehicle1 = Vehicle.objects.create(
            driver_id=self.driver1,
            make='1999',
            plate_number='AE 7777 AK',
            model='BMW'
        )
        self.vehicle2 = Vehicle.objects.create(
            driver_id=self.driver1,
            make='2005',
            plate_number='AD 1010 AK',
            model='Mercedes'
        )

        self.vehicle3 = Vehicle.objects.create(
            driver_id=None,
            make='2005',
            plate_number='AD 1010 AK',
            model='Mercedes'
        )

    def test_get_all(self):
        url = reverse('vehicles')
        response = self.client.get(url)

        serializer_data = GetVehicleSerializer([self.vehicle1, self.vehicle2, self.vehicle3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data.pop('vehicles'))

    def test_get_1(self):
        driver1 = Driver.objects.create(first_name='Ruslan', last_name='Yarovoy')
        vehicle1 = Vehicle.objects.create(
            driver_id=driver1,
            make='1999',
            plate_number='AE 7777 AK',
            model='BMW'
        )
        url = reverse('vehicle', args=[vehicle1.id])
        response = self.client.get(url, data={'vehicle1_id': vehicle1.id})

        serializer_data = GetVehicleSerializer(vehicle1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data.pop('vehicle'))

    def test_create(self):
        self.assertEqual(3, Vehicle.objects.all().count())
        data = {
            "driver_id": self.driver1.id,
            "make": "1000",
            "model": "Opel",
            "plate_number": "AE 1111 AK"
        }
        url = reverse('vehicles')
        json_data = json.dumps(data)
        response = self.client.post(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Vehicle.objects.all().count())

    def test_update(self):
        data = {
            "driver_id": self.driver1.id,
            "make": "2005",
            "model": self.vehicle1.model,
            "plate_number": self.vehicle1.plate_number
        }
        url = reverse('vehicle', args=[self.vehicle1.id])
        json_data = json.dumps(data)
        response = self.client.patch(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.vehicle1.refresh_from_db()

        self.assertEqual("2005", self.vehicle1.make)

    def test_delete(self):
        self.assertEqual(3, Vehicle.objects.all().count())
        url = reverse('vehicle', args=[self.vehicle1.id])
        response = self.client.delete(url, data={'vehicle_id': self.vehicle1.id})
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Vehicle.objects.all().count())

    def test_get_vehicles_without_driver_id(self):
        url = reverse('vehicles')
        response = self.client.get(url, data={'with_drivers': 'no'})
        serializer_data = GetVehicleSerializer(self.vehicle3).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data.pop('vehicles')[0])

    def test_get_vehicles_with_driver_id(self):
        url = reverse('vehicles')
        response = self.client.get(url, data={'with_drivers': 'yes'})
        serializer_data = GetVehicleSerializer([self.vehicle1, self.vehicle2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0], response.data.pop('vehicles')[0])

    def test_set_driver(self):
        data = {
            "driver_id": self.driver1.id,
        }
        url = reverse('vehicle_set_driver', args=[self.vehicle3.id])
        json_data = json.dumps(data)
        response = self.client.post(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.vehicle1.refresh_from_db()

        self.assertEqual(self.driver1, self.vehicle1.driver_id)



