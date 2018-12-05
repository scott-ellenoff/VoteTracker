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
from .serializers import UserSerializer, BillSerializer, LegislatorSerializer, VoteSerializer, ListVoteSerializer, MatchSerializer, CustomRegisterSerializer
from .permissions import IsAdminOrSelf, IsOwner

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, RegisterView
from rest_auth.views import LoginView

# def create_match(legislator, user):

class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        # elif self.action == 'retrieve':
            # permission_classes = [IsMatchOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.request.user.matched
            # queryset = Match.objects.all()

            # uvotes = queryset.filter(user__id=self.request.user.id)
            # lvotes = queryset.filter(legislator__isnull=False)
            # queryset = list(chain(uvotes, lvotes))

            # if self.request.user.is_anonymous:
                # queryset = uvotes
            # queryset = uvotes
            return queryset
        # elif self.action == 'user_vote':
        #     queryset = Vote.objects.all()
        #     return queryset.filter(user__id=self.request.user.id)
        else:
            return super(MatchViewSet, self).get_queryset()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAdminOrSelf,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        # m = Match.objects.all()[0]
        # print(m.user_set.all())
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):      # print(request.data)
        
        # print(request.data['followed'])
        print(kwargs)
        user = User.objects.get(pk=kwargs['pk'])
        # print(request.data)
        followed = request.data.getlist('followed')
        # print(followed)
        matched = []

        # if not followed:
        #     print('NOT', followed)
        # else:
        #     print('YES', followed)

        if not followed:
            for pm in user.matched.all():
                pm.delete()
            prev_matched = user.matched.all()
            user.matched.clear()
            # print()
            # print(prev_matched)
                # print(pm)
        request.data._mutable = True

        for l in followed:
            l_pk = l.split('/')[-2]
            legislator = Legislator.objects.get(pk=l_pk)
            print(user.followed.all()) 
            user.followed.add(legislator)
            print(user.followed.all())
            # print(legislator)
            m = Match(legislator=legislator)
            m.save()
            # print(m.MID)
            request.data.update({'matched': reverse('match-detail', args=[m.MID])})
            # user.matched.add(m)

        # print(user.followed.all())
        request.data._mutable = False
        # mutable = request.data._mutable
        # request.data._mutable = True
        # request.data['matched'] = matched
        # request.data._mutable = mutable
        # print(request.data.getlist('followed'))

        return super(UserViewSet, self).update(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     # print('PartialFlag: ', kwargs['partial'])
    #     return super(UserViewSet, self).partial_update(request, *args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        # elif self.action == 'add_vote':
        #     permission_classes = []#[IsSelf]
        else:
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]

    # def get_serializer(self, *args, *kwargs):
    #     return super(UserViewSet, self).get_serializer(args, kwargs)
    # def get_serializer_class(self, *args,):
    #     if self.action == 'add_vote':
    #         return VoteSerializer
    #     else:
    #         return UserSerializer

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
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # filter_fields = ('chamber', 'status')
    # filter_backends = (SearchFilter,)
    # search_fields = ('description')

    # def get_queryset(self):
        # """
        # Optionally restricts the returned purchases to a given user,
        # by filtering against a `username` query parameter in the URL.
        # """
        # if self.action == 'list':
            # queryset = Bill.objects.all()
            # chamber = self.request.query_params.get('user', None)
            # senator = self.request.query_params.get('senator', None)
            # fullname = self.request.query_params.get('fullname', None)

            # if chamber is not None:
                # queryset = queryset.filter(chamber=chamber)

            # if senator is not None:
            #     queryset = queryset.filter(senator=senator)

            # if fullname is not None:
            #     queryset = queryset.filter(fullname=fullname)

            # return queryset

        # else:
        # return super(BillViewSet, self).get_queryset()


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

    # def create(self, request, *args, **kwargs):
    #     return super(VoteViewSet, self).create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'user_vote' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'detail':
            permission_classes = [IsOwner]
        # elif self.action == 'user_vote':
            # permission_classes = []#[IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'detail':
            return ListVoteSerializer
        else:
            x = super(VoteViewSet, self).get_serializer_class()
            print(x)
            return x

    def get_queryset(self):
        if self.action == 'list':
            queryset = Vote.objects.all()

            legislator = self.request.query_params.get('legislator', None)
            bill = self.request.query_params.get('bill', None)

            print(legislator)
            if legislator:
                print(queryset)
                queryset = queryset.filter(legislator=legislator)
                print(queryset)

            if bill:
                queryset = queryset.filter(bill=bill)

            return queryset
            # uvotes = queryset.filter(user__id=self.request.user.id)
            # lvotes = queryset.filter(legislator__isnull=False)
            # queryset = list(chain(uvotes, lvotes))

            # if self.request.user.is_anonymous:
            #     queryset = uvotes
            # queryset = uvotes
            return queryset
        elif self.action == 'user_vote':
            queryset = Vote.objects.all()
            return queryset.filter(user__id=self.request.user.id)
        else:
            return super(VoteViewSet, self).get_queryset()

    @action(detail=False, methods=['get', 'post'], name='vote')
    def user_vote(self, request):
        if request.method == 'POST':
            # print(request.data)
            # mutable = request.data._mutable
            try:
                request.data._mutable = True
            except AttributeError:
                pass
            request.data['user'] = reverse('user-detail', args=[request.user.id])
            try:
                request.data._mutable = False
            except AttributeError:
                pass

            user = request.user
            # print(type(user))
            # print(user)
            BID = request.data.get('bill').split('/')[-2]
            b = Bill.objects.get(BID=BID)
            # print(b)
            # print(user.unvoted.all())
            user.unvoted.remove(b)
            # print(user.voted.all())
            user.voted.add(b)
            # print(user.voted.all())

            # user.unvoted.all().idrequest.data['bill']
            # print(user.unvoted.all())
            return super(VoteViewSet, self).create(request)
        elif request.method == 'GET':
            return super(VoteViewSet, self).list(request)

    # @action(detail=False, methods=['get'], name='see-vote')
    # def user_vote(self, request):
    #     mutable = request.data._mutable
    #     request.data._mutable = True
    #     request.data['user'] = reverse('user-detail', args=[request.user.id])
    #     request.data._mutable = mutable

    #     user = request.user
    #     # print(user)
    #     user.unvoted.remove(request.data['bill'])
        # return super(VoteViewSet, self).create(request)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def get_response(self):
        r = super(FacebookLogin, self).get_response()
        r.data['user'] = UserSerializer(self.user, context={'request': self.request}).data
        # r.data['user'] = reverse('user-detail', args=[self.user.id], request=self.request)
        return r

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        user.unvoted.add(*Bill.objects.all())

        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

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