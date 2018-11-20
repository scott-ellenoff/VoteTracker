from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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

    def validate(self, data):
        bill = data.get('bill')
        user = data.get('user')
        legislator = data.get('legislator')
        
        if legislator and user:
            raise serializers.ValidationError('Exactly one of user and legislator should be set.')

        try:
            if user:
                obj = Vote.objects.get(bill=bill, user=user)
            else:
                obj = Vote.objects.get(bill=bill, legislator=legislator)
            raise serializers.ValidationError('Vote already exists. Cannot duplicate vote.')
        except Vote.DoesNotExist as e:
            pass
            
        return data