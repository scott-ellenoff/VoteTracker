from django.shortcuts import render
from rest_framework import generics, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from itertools import chain
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import User, Bill, Legislator, Vote, Match
from .serializers import UserSerializer, BillSerializer, LegislatorSerializer, VoteSerializer, MatchSerializer, CustomRegisterSerializer
from .permissions import IsAdminOrSelf, IsOwner

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, RegisterView
from rest_auth.views import LoginView

# def create_match(legislator, user):

class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # permission_classes = (IsAdminOrSelf,)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAdminOrSelf,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, pk):
        # print(request.data)
        # print(request.data['followed'])
        user = User.objects.get(pk=pk)
        # print(user)
        followed = request.data.getlist('followed')
        # print(followed)
        matched = []

        request.data._mutable = True

        # print(user.matched.all())
        for pm in user.matched.all():
            pm.delete()
        prev_matched = user.matched.all()
        user.matched.clear()
        # print()
        # print(prev_matched)
            # print(pm)

        for l in followed:
            l_pk = l.split('/')[-2]
            legislator = Legislator.objects.get(pk=l_pk)
            # print(legislator)
            m = Match(legislator=legislator)
            m.save()
            # print(m.MID)
            request.data.update({'matched': reverse('match-detail', args=[m.MID])})
            # user.matched.add(m)

        request.data._mutable = False
        # mutable = request.data._mutable
        # request.data._mutable = True
        # request.data['matched'] = matched
        # request.data._mutable = mutable
        # print(request.data.getlist('followed'))

        return super(UserViewSet, self).update(request)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        
        if self.action == 'list':
            permission_classes = []#[IsAdminUser]
        # elif self.action == 'add_vote':
        #     permission_classes = []#[IsSelf]
        else:
            permission_classes = []#[IsAdminOrSelf]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'add_vote':
            return VoteSerializer
        else:
            return UserSerializer

    # @action(detail=True, methods=['post'], name='Vote')
    # def add_vote(self, request, pk):
    #     print(request.data)
    #     print(pk)
    #     # self.serializer_class = VoteSerializer
    #     mutable = request.data._mutable
    #     request.data._mutable = True
    #     request.data['user'] = reverse('user-detail', args=[pk])
    #     request.data._mutable = mutable

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     try:
    #         headers =  {'Location': str(serializer.data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         headers = {}

    #     user.unvoted.remove(request.data['bill'])

    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # return super(VoteViewSet, self).create(request)

    # def create(self, request):
    #     mutable = request.data._mutable
    #     request.data._mutable = True
    #     request.data['user'] = reverse('user-detail', args=[request.user.id])
    #     request.data._mutable = mutable

    #     user = request.user
    #     print(user.unvoted)
    #     user.unvoted.remove(request.data['bill'])
    #     print(user.unvoted)
    #     return super(VoteVi

    # @action(detail=True, methods=['put'], name='Update Unvoted')
    # def update_unvoted(self, request):
    #     user = self.get_object()
    #     serializer = UserSerializer(data = request.data)
    #     if serializer.is_valid():
    #         user.save()
    #         return Response({'status': 'unvoted updated'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

class LegislatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated,)
    queryset = Legislator.objects.all()
    serializer_class = LegislatorSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        if self.action == 'list':
            queryset = Legislator.objects.all()
            affiliation = self.request.query_params.get('affiliation', None)
            senator = self.request.query_params.get('senator', None)
            fullname = self.request.query_params.get('fullname', None)

            if affiliation is not None:
                queryset = queryset.filter(affiliation=affiliation)

            if senator is not None:
                queryset = queryset.filter(senator=senator)

            if fullname is not None:
                queryset = queryset.filter(fullname=fullname)

            return queryset

        else:
            return super(LegislatorViewSet, self).get_queryset()
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
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # filter_fields = ('chamber', 'status')
    filter_backends = (SearchFilter,)
    search_fields = ('description')



    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     if self.action == 'list':
    #         queryset = Bill.objects.all()
    #         chamber = self.request.query_params.get('chamber', None)
    #         # senator = self.request.query_params.get('senator', None)
    #         # fullname = self.request.query_params.get('fullname', None)

    #         if chamber is not None:
    #             queryset = queryset.filter(chamber=chamber)

    #         # if senator is not None:
    #         #     queryset = queryset.filter(senator=senator)

    #         # if fullname is not None:
    #         #     queryset = queryset.filter(fullname=fullname)

    #         return queryset

    #     else:
    #         return super(LegislatorViewSet, self).get_queryset()


    # filter_backends = (filters.SearchFilter)
    # search_fields = ('description', 'status', 'voted-on', 'congress-num', 'chamber', 'session', 'date-voted', 'date-introduced')

class VoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated,)
    queryset = Vote.objects.all()#.filter(owner=request.owner)
    serializer_class = VoteSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'user_vote':
            permission_classes = [IsAuthenticated]
        elif self.action == 'detail':
            permission_classes = [IsOwner]
        # elif self.action == 'user_vote':
            # permission_classes = []#[IsAuthenticated]
        else:
            permission_classes = []#[IsAdminOrSelf]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list':
            queryset = Vote.objects.all()

            uvotes = queryset.filter(user__id=self.request.user.id)
            lvotes = queryset.filter(legislator__isnull=False)
            queryset = list(chain(uvotes, lvotes))
            # queryset = uvotes

            return queryset

        else:
            return super(VoteViewSet, self).get_queryset()

    @action(detail=False, methods=['post'], name='Vote')
    def user_vote(self, request):
        mutable = request.data._mutable
        request.data._mutable = True
        request.data['user'] = reverse('user-detail', args=[request.user.id])
        request.data._mutable = mutable

        user = request.user
        # print(user)
        user.unvoted.remove(request.data['bill'])
        return super(VoteViewSet, self).create(request)

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