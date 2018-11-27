import datetime
import random
import string
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login

def create_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class User(AbstractUser):
    class Meta:
        db_table = 'Users'

    UID = models.UUIDField(db_column='UID', max_length=12, default=uuid.uuid4, editable=False)
    name = models.TextField(db_column='Name', blank=True, null=True)
    district = models.IntegerField(db_column='District', blank=True, null=True)
    matched = models.ManyToManyField('Legislator', related_name='matched', blank=True)
    followed = models.ManyToManyField('Legislator', related_name='followed', blank=True)

# @receiver(pre_social_login)
# def save_user(sender, request, sociallogin, **kwargs):
#     print(kwargs)
#     print(vars(request))
#     print(vars(sociallogin))
#     print(sender)

@receiver(user_signed_up)
def on_user_signed_up(request, user, sociallogin=None, **kwargs):

    if sociallogin:

        if sociallogin.account.provider == 'facebook':
            print(user)
            print(sociallogin.serialize())
            print(sociallogin.account.extra_data)
            # user.email = sociallogin.account.extra_data['email']
            try:
                user.email = sociallogin.account.extra_data['email']
            except KeyError:
                user.email = 'no@email.com'
            user.name = sociallogin.account.extra_data['first_name'] + \
                ' ' + sociallogin.account.extra_data['last_name']
            user.save()
            # name = sociallogin.account.extra_data['name']
            # user.email = sociallogin.account.extra_data['email']
            # user.save()
            # if sociallogin.account.extra_data['gender'] == 'male':
            #     gender = 'M'
            # elif sociallogin.account.extra_data['gender'] == 'female':
            #     gender = 'F'
            # user.create_profile(fullname=name, gender=gender)


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


    BID = models.CharField(db_column='BID', max_length=12, default=create_random_id, primary_key=True, editable=False)
    description = models.TextField(db_column='Description', blank=True)
    date_introduced = models.DateField(db_column='DateIntroduced', default=datetime.date.today)
    status = models.TextField(db_column='Status', choices=BILL_STATUS, blank=True)
    voted_on = models.BooleanField(db_column='VotedOn', blank=True, null=True)
    congress_num = models.IntegerField(db_column='CongressN', blank=True, null=True)
    chamber = models.CharField(db_column='Chamber', max_length=10, choices=CHAMBERS, blank=True)
    session = models.IntegerField(db_column='Session', blank=True, null=True)
    date_voted = models.DateField(db_column='DateVoted', default=datetime.date.today, blank=True)
    url = models.URLField(db_column='URL', blank=True, null=True)

class Legislator(models.Model):
    class Meta:
        db_table = 'Legislators'

    AFFILIATION = (
            ('D', 'Democrat'),
            ('R', 'Republican'),
            ('I', 'Independent'),
            ('O', 'Other')
    )
    LID = models.CharField(db_column='LID', max_length=12, default=create_random_id, primary_key=True, editable=False)
    fullname = models.CharField(db_column='FullName', max_length=255, blank=True)
    senator = models.BooleanField(db_column='isSenator', blank=True, null=True)
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

    VID = models.UUIDField(db_column='ID', default=uuid.uuid4, primary_key=True, editable=False)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, blank=True, null=True)
    legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    vote = models.CharField(max_length=1, choices=VOTES, blank=True)

    def save(self, *args, **kwargs):
        if self.user and self.legislator or not self.user and not self.legislator:
            raise ValueError('Exactly one of [Vote.user, Vote.legislator] must be set')

        super(Vote, self).save(*args, **kwargs)