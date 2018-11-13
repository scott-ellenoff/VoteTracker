from django.db import models
import datetime

class Bill(models.Model):
    BILL_STATUS = (
        ('P', 'Passed'),
        ('R', 'Rejected'),
        ('OTF', 'On the Floor'),
        ('IC', 'In committee')
    )

    CHAMBERS = (
        ('S', 'Senate'),
        ('H', 'House of Representatives')
    )

    BID = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    short_descr = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    date_intr = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=3, choices=BILL_STATUS, blank=True)
    voted_on = models.BooleanField(null=True)
    chamber = models.CharField(max_length=1, choices=CHAMBERS, blank=True)
    session = models.IntegerField(null=True)
    roll_call_ID = models.IntegerField(null=True)
    date_voted = models.DateField(default=datetime.date.today)
    url = models.URLField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.BID, self.name)

