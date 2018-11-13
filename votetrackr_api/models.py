import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    UID = models.IntegerField(null=True)
    district = models.CharField(max_length=30, blank=True)

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

class Legislator(models.Model):
  AFFILIATION = (
        ('D', 'Democrat'),
        ('R', 'Republican'),
        ('I', 'Independent'),
        ('O', 'Other')
  )
  LID = models.IntegerField()
  name = models.CharField(max_length=255, blank=True)
  senator = models.BooleanField(null=True)
  affiliation = models.CharField(max_length=1, choices=AFFILIATION, blank=True)
  district = models.IntegerField()
  URL = models.URLField(blank=True)


class Vote(models.Model):
  VOTES = (
        ('Y', 'Yea'),
        ('N', 'Nay'),
        ('A', 'Abstain')
  )
  LID = models.IntegerField()
  UID = models.IntegerField()
  BID = models.IntegerField()
  vote = models.CharField(max_length=1, choices=VOTES, blank=True)
