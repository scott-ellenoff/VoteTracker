from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from rest_framework.validators import UniqueTogetherValidator

from rest_auth.registration.serializers import RegisterSerializer

from .models import User, Bill, Legislator, Vote, Match

class UserSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='user-detail')
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'UID', 'name', 'district', 'unvoted', 'voted', 'matched', 'followed', 'detail')

class BillSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='bill-detail')
    class Meta:
        model = Bill
        fields = ('BID', 'name', 'description', 'date_introduced', 'status', 'voted_on', 'chamber', 'date_voted', 'url', 'detail')


class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='legislator-detail')
    class Meta:
        model = Legislator
        fields = ('LID', 'fullname', 'district', 'state', 'senator', 'affiliation', 'dwnominate', 'url', 'detail')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='vote-detail')
    bill = BillSerializer(read_only=True)
    class Meta:
        model = Vote
        fields = ('VID', 'bill', 'legislator', 'user', 'vote', 'detail')

    def validate(self, data):
        bill = data.get('bill', None)
        user = data.get('user', None)
        legislator = data.get('legislator')
        
        if legislator and user:
            raise serializers.ValidationError('Exactly one of user and legislator should be set.')

        try:
            if user:
                obj = Vote.objects.get(bill=bill, user=user)
                # if obj.user == user:
                raise serializers.ValidationError('Vote already exists. Cannot duplicate vote.')
            else:
                obj = Vote.objects.get(bill=bill, legislator=legislator)
                raise serializers.ValidationError('Vote already exists. Cannot duplicate vote.')
            # if obj:
            #     print(obj)
            #     raise serializers.ValidationError('Vote already exists. Cannot duplicate vote.')
        except Vote.DoesNotExist as e:
            pass
            
        return data

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    detail = HyperlinkedIdentityField(view_name='match-detail')
    class Meta:
        model = Match
        fields = ('MID', 'legislator', 'match_percentage', 'num_votes', 'detail')

class CustomRegisterSerializer(RegisterSerializer):
    UID = serializers.UUIDField(read_only=True)
    district = serializers.IntegerField()
    name = serializers.CharField()

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.district = self.validated_data.get('district', '')
        user.save()