import pytz
from django.db import models
from driver.models import Driver


class Vehicle(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255, verbose_name='Model')
    plate_number = models.CharField(max_length=255, verbose_name='Plate Number')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    driver_id = models.ForeignKey(
        Driver,
        related_name='vehicles',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'vehicles'
        ordering = ['make', 'model', 'plate_number']

    def __repr__(self) -> str:
        class_name: str = self.__class__.__name__
        created: str = self.created_at.astimezone(pytz.UTC).isoformat()
        updated: str = self.updated_at.astimezone(pytz.UTC).isoformat()

        return f'<{class_name} (' \
               f'id={self.id}, ' \
               f'make={self.make}, ' \
               f'model={self.model}, ' \
               f'plate_number={self.plate_number}, ' \
               f'driver_id={self.driver_id}, ' \
               f'created={created}, ' \
               f'updated={updated})>'
