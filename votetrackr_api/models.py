from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    UID = models.IntegerField(null=True)
    district = models.CharField(max_length=30, blank=True)

class Bill(models.Model):
    BID = models.IntegerField()
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.BID, self.name)

