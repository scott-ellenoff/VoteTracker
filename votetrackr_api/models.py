from django.db import models

class Bill(models.Model):
    BID = models.IntegerField()
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.BID, self.name)