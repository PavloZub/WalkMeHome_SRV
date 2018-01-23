from django.db import models

# Create your models here.
from django.db import models


class LocationData(models.Model):
    def __str__(self):
        return "{email} | {date} | {LAT} | {LON}".format(email=self.email, date=self.loc_date, LAT=self.LAT, LON=self.LON)
    email = models.CharField(max_length=30)
    loc_date = models.DateTimeField('location date')
    LAT = models.FloatField(default=0)
    LON = models.FloatField(default=0)
