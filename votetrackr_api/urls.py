from django.urls import path
from .views import ListUserView, ListBillView, ListLegislatorView, ListVoteView


urlpatterns = [
    path('user/', ListUserView.as_view(), name='user-all'),
    path('bill/', ListBillView.as_view(), name="bill-all"),
    path('legislator/', ListLegislatorView.as_view(), name='legislator-all'),
    path('vote/', ListVoteView.as_view(), name='vote-all'),
]