import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'Users'

    UID = models.UUIDField(db_column='UID', default=uuid.uuid4, editable=False)
    district = models.CharField(max_length=30, blank=True)

class Bill(models.Model):
    class Meta:
        db_table = 'Bills'

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


    BID = models.UUIDField(db_column='BID', default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField(db_column='Description', blank=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True)
    date_introduced = models.DateField(db_column='DateIntroduced', default=datetime.date.today)
    status = models.CharField(db_column='Status', max_length=50, choices=BILL_STATUS, blank=True)
    voted_on = models.BooleanField(db_column='VotedOn', blank=True, null=True)
    congress_num = models.IntegerField(db_column='CongressN', blank=True, null=True)
    chamber = models.CharField(db_column='Chamber', max_length=10, choices=CHAMBERS, blank=True)
    session = models.IntegerField(db_column='Session', blank=True, null=True)
    date_voted = models.DateField(db_column='DateVoted', default=datetime.date.today, blank=True)
    roll_call_ID = models.IntegerField(db_column='RollCallID', blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.BID, self.name)

class Legislator(models.Model):
    class Meta:
        db_table = 'Legislators'

    AFFILIATION = (
            ('D', 'Democrat'),
            ('R', 'Republican'),
            ('I', 'Independent'),
            ('O', 'Other')
    )
    LID = models.UUIDField(db_column='LID', default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(db_column='Name', max_length=255, blank=True)
    senator = models.BooleanField(db_column='Senator?', blank=True, null=True)
    affiliation = models.TextField(db_column='Affiliation', choices=AFFILIATION, blank=True, null=True)
    dwnominate = models.FloatField(db_column='DWNominate', blank=True, null=True)
    url = models.URLField(db_column='URL', blank=True, null=True)


class Vote(models.Model):
    class Meta:
        db_table = 'Votes'

    VOTES = (
        ('Y', 'Yea'),
        ('N', 'Nay'),
        ('A', 'Abstain')
    )
    VID = models.IntegerField(db_column='ID', primary_key=True)
    LID = models.IntegerField(db_column='LorU', blank=True, null=True)
    UID = models.IntegerField(db_column='UID', unique=True, max_length=20)
    BID = models.IntegerField()
    vote = models.CharField(max_length=1, choices=VOTES, blank=True)
