from django.urls import path
from .views import ListBillView


urlpatterns = [
    path('bill/', ListBillView.as_view(), name="bill-all")
]