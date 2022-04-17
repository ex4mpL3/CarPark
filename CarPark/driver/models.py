import pytz

from django.db import models


class Driver(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    class Meta:
        db_table = 'drivers'
        ordering = ['first_name', 'last_name']

    def __repr__(self) -> str:
        class_name: str = self.__class__.__name__
        created: str = self.created_at.astimezone(pytz.UTC).isoformat()
        updated: str = self.updated_at.astimezone(pytz.UTC).isoformat()

        return f'<{class_name} (' \
               f'id={self.id}, ' \
               f'first_name={self.first_name}, ' \
               f'last_name={self.last_name}, ' \
               f'created={created}, ' \
               f'updated={updated})>'
