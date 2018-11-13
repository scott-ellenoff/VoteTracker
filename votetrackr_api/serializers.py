from rest_framework import serializers
from .models import User, Bill, Legislator, Vote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'UID', 'district')

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('BID', 'short-descr', 'category', 'date_intr', 'status', 'voted_on', 'chamber', 'session', 'roll_call_ID','date_voted', 'url')


class LegislatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legislator
        fields = ('LID', 'name', 'senator', 'affiliation', 'district', 'URL')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('LID', 'UID', 'BID', 'vote')