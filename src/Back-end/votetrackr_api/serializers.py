from rest_framework import serializers
from .models import User, Bill, Legislator, Vote

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'UID', 'name', 'district', 'matched', 'followed')

class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ('BID', 'description', 'date_introduced', 'status', 'voted_on', 'chamber', 'session', 'date_voted', 'url')


class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator
        fields = ('LID', 'fullname', 'senator', 'affiliation', 'dwnominate', 'url')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('VID', 'bill', 'legislator', 'user', 'vote')