from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import User, Bill, Legislator, Vote
from .serializers import UserSerializer, BillSerializer, LegislatorSerializer, VoteSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LegislatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Legislator.objects.all()
    serializer_class = LegislatorSerializer

class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class VoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

# # Create your views here.
# class ListUserView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ListBillView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = Bill.objects.all()
#     serializer_class = BillSerializer


# class ListLegislatorView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = Legislator.objects.all()
#     serializer_class = LegislatorSerializer


# class ListVoteView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer