from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.reverse import reverse, reverse_lazy
from .models import User, Bill, Legislator, Vote
from .serializers import UserSerializer, BillSerializer, LegislatorSerializer, VoteSerializer, CustomRegisterSerializer
from .permissions import IsAdminOrSelf

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, RegisterView
from rest_auth.views import LoginView

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    permission_classes = (IsAdminOrSelf,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class LegislatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated,)
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
    # permission_classes = (IsAuthenticated,)
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    # filter_backends = (filters.SearchFilter)
    # search_fields = ('description', 'status', 'voted-on', 'congress-num', 'chamber', 'session', 'date-voted', 'date-introduced')

class VoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def get_response(self):
        r = super(FacebookLogin, self).get_response()
        r.data['user'] = UserSerializer(self.user, context={'request': self.request}).data
        # r.data['user'] = reverse('user-detail', args=[self.user.id], request=self.request)
        return r

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def get_response_data(self, user):
        data = super(CustomRegisterView, self).get_response_data(user)
        data['user'] = UserSerializer(user, context={'request': self.request}).data
        return data

class CustomLoginView(LoginView):
    def get_response(self):
        r = super(CustomLoginView, self).get_response()
        r.data['user'] = UserSerializer(self.user, context={'request': self.request}).data
        return r

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
