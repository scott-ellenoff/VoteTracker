from rest_framework import serializers
from .models import Bill, Legislator, Vote

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('BID', 'name', 'short-descr', 'category', 'date_intr', 'status', 'voted_on', 'chamber', 'session', 'roll_call_ID','date_voted', 'url')


class LegislatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legislator
        fields = ('LID', 'name', 'senator', 'affiliation', 'district', 'URL')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('LID', 'UID', 'BID', 'vote')