from django.shortcuts import render
from rest_framework import generics
from .models import Bill, Legislator, Vote
from .serializers import BillSerializer, LegislatorSerializer, VoteSerializer

# Create your views here.
class ListBillView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class ListLegislatorView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Legislator.objects.all()
    serializer_class = LegislatorSerializer


class ListVoteView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer