from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import User, Bill, Legislator, Vote
from .serializers import UserSerializer, BillSerializer, LegislatorSerializer, VoteSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
        
    #     permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

class LegislatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Legislator.objects.all()
    serializer_class = LegislatorSerializer

    # def get_queryset(self):
    #     try:
    #         legislator = self.request.legislator
    #         return Legislator.objects.filter(legislator=legislator)
    #     except:
    #         return None

    # filter_backends = (filters.SearchFilter)
    # search_fields = ('legislator', 'name', 'affiliation')

class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    # filter_backends = (filters.SearchFilter)
    # search_fields = ('description', 'status', 'voted-on', 'congress-num', 'chamber', 'session', 'date-voted', 'date-introduced')

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