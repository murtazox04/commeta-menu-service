from django.db import models

from apps.common.models import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    working_time = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'restaurants'
        managed = False

    def __str__(self):
        return self.name
