from rest_framework import serializers
from .models import Bill


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('BID', 'name', 'short-descr', 'category', 'date_intr', 'status', 'voted_on', 'chamber', 'session', 'roll_call_ID','date_voted', 'url')