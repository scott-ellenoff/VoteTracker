from django.urls import path
from django.conf.urls import url, include
# from .views import ListUserView, ListBillView, ListLegislatorView, ListVoteView
from .views import UserViewSet, BillViewSet, LegislatorViewSet, VoteViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bills', BillViewSet)
router.register(r'legislators', LegislatorViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]

# urlpatterns = [
#     path('user/', ListUserView.as_view(), name='user-all'),
#     path('bill/', ListBillView.as_view(), name="bill-all"),
#     path('legislator/', ListLegislatorView.as_view(), name='legislator-all'),
#     path('vote/', ListVoteView.as_view(), name='vote-all'),
# ]