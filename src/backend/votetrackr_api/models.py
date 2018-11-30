import datetime
import random
import string
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login

def create_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


# class CustomUserManager(UserManager):
    # def create_user(username, email=None, password=None, **extra_fields):
    #     print('asdf;laksdfjas')
        # return super(CustomUserManager, self).create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    class Meta:
        db_table = 'Users'

    # objects = CustomUserManager()
    UID = models.UUIDField(db_column='UID', max_length=12, default=uuid.uuid4, editable=False)
    name = models.TextField(db_column='Name', blank=True, null=True)
    district = models.IntegerField(db_column='District', blank=True, null=True)
    # matched = models.ForeignKey('Match', on_delete=models.CASCADE, blank=True, null=True)
    matched = models.ManyToManyField('Match', related_name='matched', blank=True)
    followed = models.ManyToManyField('Legislator', related_name='followed', blank=True)
    unvoted = models.ManyToManyField('Bill', related_name='unvoted', blank=True)
    voted = models.ManyToManyField('Bill', related_name='voted', blank=True)



    def calculate_matches(self):
        for m in self.matched.all():
            m.calculate()

    def save(self, *args, **kwargs):
        # print(locals())
        # if self.user:
        #     for l in self.user.followed():
        #         print(l)
        #         Vote.objects.filter(legislator=self.legislator).filter(bill=self.bill)
        #         match = u.matched.filter(Legislator = self.legislator)
        #         match.numberOfVotes = match.numberOfVotes+1
        #         if self.vote == lVote.vote:
        #             match.matchPercentage = match.matchPercentage + (1-match.matchPercentage)/(match.numberOfVotes)
        #         else:
        #             match.matchPercentage = match.mmatchPercentage + (0-match.matchPercentage)/(match.numberOfVotes)
        #         match.save()

        super(User, self).save(*args, **kwargs)

    # def compute_matches():

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

class Match(models.Model):
    class Meta:
        db_table = 'Matches'

    MID = models.UUIDField(db_column='MID', default=uuid.uuid4, editable=False, primary_key=True)
    legislator = models.ForeignKey('Legislator', on_delete=models.CASCADE, blank=True, null=True)
    match_percentage = models.DecimalField(db_column='Percentage', decimal_places=4, max_digits=6, default=0)
    num_votes = models.IntegerField(db_column='NumVotes', default=0)

    def calculate(self):
        user = User.objects.get(matched__MID=self.MID)
        legislator = self.legislator

        uvotes = Vote.objects.filter(user=user)
        total_count = 0
        same_count = 0
        for user_vote in uvotes:
            try:
                leg_vote = Vote.objects.get(legislator=legislator, bill=user_vote.bill)
            except Vote.DoesNotExist:
                leg_vote = None
            if leg_vote:
                total_count += 1
                same_count += user_vote.vote == leg_vote.vote
        self.num_votes = total_count
        self.match_percentage = same_count / total_count
        self.save()

class Bill(models.Model):
    class Meta:
        db_table = 'Bills'

    # BILL_STATUS = (
    #     ('Passed', 'Passed'),
    #     ('Rejected', 'Rejected'),
    #     ('On the Floor', 'On the Floor'),
    #     ('In Commitee', 'In committee')
    # )

    CHAMBERS = (
        ('Senate', 'Senate'),
        ('House', 'House of Representatives')
    )


    BID = models.CharField(db_column='BID', max_length=12, default=create_random_id, primary_key=True, editable=True)
    name = models.TextField(db_column='Name', blank=True)
    description = models.TextField(db_column='Description', blank=True)
    date_introduced = models.DateField(db_column='DateIntroduced', default=datetime.date.today)
    status = models.TextField(db_column='Status', blank=True)
    voted_on = models.BooleanField(db_column='VotedOn', blank=True, null=True)
    congress_num = models.IntegerField(db_column='CongressN', blank=True, null=True)
    chamber = models.CharField(db_column='Chamber', max_length=10, choices=CHAMBERS, blank=True)
    date_voted = models.DateField(db_column='DateVoted', default=datetime.date.today, blank=True)
    url = models.URLField(db_column='URL', blank=True, null=True)

class Legislator(models.Model):
    class Meta:
        db_table = 'Legislators'

    AFFILIATION = (
            ('Democrat', 'Democrat'),
            ('Republican', 'Republican'),
            ('Independent', 'Independent'),
            ('Other', 'Other')
    )
    LID = models.CharField(db_column='LID', max_length=12, default=create_random_id, primary_key=True, editable=True)
    fullname = models.CharField(db_column='FullName', max_length=255, blank=True)
    senator = models.BooleanField(db_column='isSenator', blank=True, null=True)
    affiliation = models.TextField(db_column='Affiliation', choices=AFFILIATION, blank=True, null=True)
    district = models.IntegerField(db_column='District', blank=True, null=True)
    state = models.CharField(db_column='State', max_length=20, blank=True)
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
        if self.user:
            self.user.calculate_matches()
        #     for l in self.user.followed():
        #         print(l)
        #         Vote.objects.filter(legislator=self.legislator).filter(bill=self.bill)
        #         match = u.matched.filter(Legislator = self.legislator)
        #         match.numberOfVotes = match.numberOfVotes+1
        #         if self.vote == lVote.vote:
        #             match.matchPercentage = match.matchPercentage + (1-match.matchPercentage)/(match.numberOfVotes)
        #         else:
        #             match.matchPercentage = match.mmatchPercentage + (0-match.matchPercentage)/(match.numberOfVotes)
        #         match.save()

        super(Vote, self).save(*args, **kwargs)
