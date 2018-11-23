from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from rest_framework.validators import UniqueTogetherValidator

from .models import User, Bill, Legislator, Vote

class UserSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='user-detail')
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'UID', 'name', 'district', 'matched', 'followed', 'detail')

class BillSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='bill-detail')
    class Meta:
        model = Bill
        fields = ('BID', 'description', 'date_introduced', 'status', 'voted_on', 'chamber', 'session', 'date_voted', 'url', 'detail')


class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='legislator-detail')
    class Meta:
        model = Legislator
        fields = ('LID', 'fullname', 'senator', 'affiliation', 'dwnominate', 'url', 'detail')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='vote-detail')
    class Meta:
        model = Vote
        fields = ('VID', 'bill', 'legislator', 'user', 'vote', 'detail')

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