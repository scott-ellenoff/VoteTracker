from django.urls import path
from django.conf.urls import url, include
# from .views import ListUserView, ListBillView, ListLegislatorView, ListVoteView
from .views import UserViewSet, BillViewSet, LegislatorViewSet, VoteViewSet, FacebookLogin, CustomRegisterView, CustomLoginView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bills', BillViewSet)
router.register(r'legislators', LegislatorViewSet)
router.register(r'votes', VoteViewSet)
# router.register(r'rest-auth/register', CustomRegisterView)
# router.register(r'rest-auth/login/', CustomLoginView)
# router.register(r'rest-auth/facebook/', FacebookLogin)
# print(include(router.urls))
urlpatterns = [
    path('', include(router.urls)),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('registration/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login/facebook/', FacebookLogin.as_view(), name='fb_login'),
]

# urlpatterns = [
#     path('user/', ListUserView.as_view(), name='user-all'),
#     path('bill/', ListBillView.as_view(), name="bill-all"),
#     path('legislator/', ListLegislatorView.as_view(), name='legislator-all'),
#     path('vote/', ListVoteView.as_view(), name='vote-all'),
# ]