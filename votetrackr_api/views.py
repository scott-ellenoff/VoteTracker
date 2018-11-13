from django.shortcuts import render
from rest_framework import generics
from .models import Bill
from .serializers import BillSerializer

# Create your views here.
class ListBillView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer