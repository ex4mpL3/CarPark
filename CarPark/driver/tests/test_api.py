import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from driver.models import Driver
from driver.serializers import DriversSerializer


class DriverApiTestCase(APITestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(first_name='Ruslan', last_name='Yarovoy')
        self.driver2 = Driver.objects.create(first_name='Roman', last_name='Yarovoy')

    def test_get_all(self):
        url = reverse('drivers')
        response = self.client.get(url)

        serializer_data = DriversSerializer([self.driver2, self.driver1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data.pop('drivers'))

    def test_get_1(self):
        url = reverse('driver', args=[self.driver1.id])
        response = self.client.get(url, data={'driver_id': self.driver1.id})

        serializer_data = DriversSerializer(self.driver1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data.pop('driver'))

    def test_create(self):
        self.assertEqual(2, Driver.objects.all().count())
        url = reverse('drivers')
        data = {
            "first_name": "Johnny",
            "last_name": "Depp"
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Driver.objects.all().count())

    def test_update(self):
        url = reverse('driver', args=[self.driver1.id])
        data = {
            "first_name": self.driver1.first_name,
            "last_name": "Depp"
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.driver1.refresh_from_db()
        self.assertEqual("Depp", self.driver1.last_name)

    def test_delete(self):
        self.assertEqual(2, Driver.objects.all().count())
        url = reverse('driver', args=[self.driver1.id])
        response = self.client.delete(url, data={'driver_id': self.driver1.id})

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Driver.objects.all().count())
