from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from rest_framework.authtoken.models import Token
from votetrackr_api.models import User, Bill, Legislator, Vote
from votetrackr_api.db_updater import db_updater
# Create your tests here.
import unittest
import json

BASE_URL = 'http://testserver/api/v1/'
REGISTER_URL = 'http://testserver/api/v1/registration/'
LOGIN_URL = 'http://testserver/api/v1/login/'
VOTES_LEGISLATOR_URL = 'http://testserver/api/v1/votes/'
VOTES_USER_URL = 'http://testserver/api/v1/votes/user_vote/'
BILLS_URL = 'http://testserver/api/v1/bills/'
USERS_URL = 'http://testserver/api/v1/users/'
LEGISLATOR_URL = 'http://testserver/api/v1/legislators/'
MATCHES_URL = 'http://testserver/api/v1/matches/'

TEST_FILE = open('votetrackr_api/test_data.json')
TEST_DATA = json.load(TEST_FILE)


class UserTests(APITestCase):
    def test_user(self):
        # user data to be reused
        user_data = {"username": "cc",
                     "name" : "Comps Cience", 
                     "district": "10128", 
                     "email": "qrs@gmail.com", 
                     "password1": "thisis220", 
                     "password2": "thisis220"}

        legislator_data = {"username":"cc",
                           "name": "L. Ron Hubbard", 
                           "district":"60615"}

        # add a user
        response = self.client.post(REGISTER_URL, user_data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # attempting to add duplicate user 
        response = self.client.post(REGISTER_URL, user_data, format="json")
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_endpoint = USERS_URL+realUID+'/'

        # testing getting user without properly authenticating
        response = self.client.get(user_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=realUID)
        client = self.client
        client.force_authenticate(user=user)

        # testing getting user after properly authenticating
        response = self.client.get(user_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # setting info
        response = self.client.put(user_endpoint, legislator_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # removing a user
        response.client.delete(user_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bill(self):
        bills = TEST_DATA['bills']
        
        # Setting authentication
        user_data = {
            'username': 'admin',
            'name' : 'Admin', 
            'district': '0', 
            'email': 'votetrackr18@gmail.com', 
            'password1': 'thisis220', 
            'password2': 'thisis220'
        }

        response = self.client.post(REGISTER_URL, user_data, format='json')
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=realUID)
        user.is_staff = True
        user.save()
        self.client.force_authenticate(user=user)

        # testing adding a Bill
        response = self.client.post(BILLS_URL, bills[0])
        response_body = json.loads(response.content)
        realBID = response_body['BID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bill_url = BILLS_URL + '{}/'.format(realBID)

        # changing a Bill status
        data = bills[0]
        data['name'] = 'New bill name'
        response = self.client.put(bill_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_body = json.loads(response.content)
        self.assertEqual(response_body['name'], 'New bill name')

        #deleting a bill
        response.client.delete(bill_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get bill on removed bill
        response = self.client.get(bill_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_legislator(self):
        legislators = TEST_DATA['legislators']

        # Setting authentication
        user_data = {
            'username': 'admin',
            'name' : 'Admin', 
            'district': '0', 
            'email': 'votetrackr18@gmail.com', 
            'password1': 'thisis220', 
            'password2': 'thisis220'
        }

        response = self.client.post(REGISTER_URL, user_data, format='json')
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=realUID)
        user.is_staff = True
        user.save()
        self.client.force_authenticate(user=user)

        #testing adding legislator
        response = self.client.post(LEGISLATOR_URL, legislators[0], format="json")
        response_body = json.loads(response.content)
        realLID = str(response_body['LID'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        legislator_url = LEGISLATOR_URL + '{}/'.format(realLID)

        data = legislators[0]
        data['fullname'] = 'Yuxi Chen'
        data['url'] = 'http://www.google.com'
        response = self.client.put(legislator_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_body = json.loads(response.content)
        self.assertEqual(response_body['fullname'], 'Yuxi Chen')
        self.assertEqual(response_body['url'], 'http://www.google.com')

        #deleting a legislator
        response.client.delete(legislator_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get legislator on removed legislator
        response = self.client.get(legislator_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vote(self):
        bills = TEST_DATA['bills']
        legislators = TEST_DATA['legislators']
        votes = TEST_DATA['votes']

        # Create admin user to populate database
        user_data = {
            'username': 'admin',
            'name' : 'Admin', 
            'district': '0', 
            'email': 'votetrackr18@gmail.com', 
            'password1': 'thisis220', 
            'password2': 'thisis220'
        }

        response = self.client.post(REGISTER_URL, user_data, format='json')
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=realUID)
        user.is_staff = True
        user.save()
        self.client.force_authenticate(user=user)

        # Populate database
        for bill in bills:
            response = self.client.post(BILLS_URL, bill)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for legislator in legislators:
            response = self.client.post(LEGISLATOR_URL, legislator)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for vote in votes:
            response = self.client.post(VOTES_LEGISLATOR_URL, vote)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_data = {
            'username': 'shanlu',
            'name' : 'Shan Lu', 
            'district': '0', 
            'email': 'shanlu@gmail.com', 
            'password1': 'thisis220', 
            'password2': 'thisis220'
        }

        # Register User
        response = self.client.post(REGISTER_URL, user_data, format='json')
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authenticate user
        user = User.objects.get(id=realUID)
        self.client.force_authenticate(user=user)

        # Unvoted should have all bills, voted should have no bills after user is first created
        unvoted = response_body['user']['unvoted']
        voted = response_body['user']['voted']
        self.assertEqual(unvoted, [BILLS_URL + '{}/'.format(bill['BID']) for bill in bills])
        self.assertEqual(voted, [])

        # Check voted and unvoted bills list after each vote
        for i, bill in enumerate(bills):
            vote_data = {'bill': '/api/v1/bills/{}/'.format(bill['BID']), 'vote': 'Y'}
            response = self.client.post(VOTES_USER_URL, vote_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response = self.client.get(USERS_URL + realUID + '/', format='json')
            response_body = json.loads(response.content)
            unvoted = response_body['unvoted']
            voted = response_body['voted']

            # Test bill added to voted bills
            self.assertEqual(voted, [BILLS_URL + bill['BID'] + '/' for bill in bills[:i + 1]])
            # Test bill removed from unvoted bills
            self.assertEqual(unvoted, [BILLS_URL + bill['BID'] + '/' for bill in bills[i + 1:]])

    def test_permissions(self):
        data = {"username": "user1",
                "name" : "First Last", 
                "district" : "10001", 
                "email" : "qxy@gmail.com", 
                "password1": "pa$$w0rdy",
                "password2": "pa$$w0rdy"}

        # Registrate the user we'll test
        response = self.client.post(REGISTER_URL, data, format="json")
        response_body = json.loads(response.content)
        realUID1 = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        other_user = {"username": "user09",
                      "name" : "Firstname Lastname", 
                      "district" : "10001", 
                      "email" : "lmn@gmail.com", 
                      "password1": "s0ftwar3",
                      "password2": "s0ftwar3"}

        # Registrate a second user to test against
        response = self.client.post(REGISTER_URL, other_user, format="json")
        response_body = json.loads(response.content)
        realUID2 = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user1_url = USERS_URL+realUID1+'/'
        user2_url = USERS_URL+realUID2+'/'

        #testing getting user without authentication
        response = self.client.get(user1_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #testing getting user on failed login
        response = self.client.get(user1_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login with incorrect password
        wrong_data = {"username": "user1", "password": "passwordy"}
        response = self.client.post(LOGIN_URL, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Authenticate
        user = User.objects.get(id=realUID1)
        user.save()
        self.client.force_authenticate(user=user)
        
        # Getting user info after authenticated
        response = self.client.get(user1_url)
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Getting the other user info after authenticated
        response = self.client.get(user2_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Getting user list view after authenticated if not staff
        response = self.client.get(USERS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # logout
        self.client.force_authenticate(user=None)

        # Testing getting user info after logout
        response = self.client.get(user1_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Getting user list view after logout
        response = self.client.get(USERS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_match(self):
        bills = TEST_DATA['bills']
        legislators = TEST_DATA['legislators']
        votes = TEST_DATA['votes']

        # Create admin user to populate database
        user_data = {
            'username': 'admin',
            'name' : 'Admin', 
            'district': '0', 
            'email': 'votetrackr18@gmail.com', 
            'password1': 'thisis220', 
            'password2': 'thisis220'
        }

        response = self.client.post(REGISTER_URL, user_data, format='json')
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=realUID)
        user.is_staff = True
        user.save()
        self.client.force_authenticate(user=user)

        # Populate database
        for bill in bills:
            response = self.client.post(BILLS_URL, bill)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for legislator in legislators:
            response = self.client.post(LEGISLATOR_URL, legislator)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for vote in votes:
            response = self.client.post(VOTES_LEGISLATOR_URL, vote)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_data = {
            'username': 'shanlu',
            'name' : 'Shan Lu', 
            'district': '0', 
            'email': 'shanlu@gmail.com', 
            'password1': 'thisis220', 
            'password2': 'thisis220'
        }

        response = self.client.post(REGISTER_URL, user_data, format='json')
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authenticating user
        user = User.objects.get(id=realUID)
        self.client.force_authenticate(user=user)

        user_data = response_body['user']
        user_url = USERS_URL + '{}/'.format(realUID)

        # There should be no matches before following
        response = self.client.get(MATCHES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_body = json.loads(response.content)
        self.assertEqual(response_body, [])

        # Add all legislators to followed
        followed = ['/api/v1/legislators/{}/'.format(legislator['LID']) for legislator in legislators]
        user_data['followed'] = followed
        response = self.client.put(user_url, user_data, fromat='json')
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['followed'], ['http://testserver' + legislator for legislator in followed])

        # Match percentages before voting should all be zero
        response = self.client.get(MATCHES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_body = json.loads(response.content)
        for m in response_body:
            self.assertEqual(float(m['match_percentage']), 0.0)

        # Vote yes on every bill
        for bill in bills:
            vote_data = {'bill': '/api/v1/bills/{}/'.format(bill['BID']), 'vote': 'Y'}
            response = self.client.post(VOTES_USER_URL, vote_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response = self.client.get(USERS_URL + realUID + '/', format='json')
            response_body = json.loads(response.content)

        # Check match percentages after voting
        match_percentages = [0.75, 0.50, 0.75, 0.50, 0.00]
        correct_matches = {LEGISLATOR_URL + '{}/'.format(l['LID']): p for l, p in zip(legislators, match_percentages)}
        response = self.client.get(MATCHES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_body = json.loads(response.content)
        for m in response_body:
            self.assertEqual(float(m['match_percentage']), correct_matches[m['legislator']])

# class UpdaterTests(APITestCase):
#     def test_updater(self):
#         newUpdater = db_updater()

#         # Testing whether the updater can successfully update database with new votes and bills
#         # Returns false if cannot connect to API: either key is old, or API changed the input format - cannot unit test
#         # that since the inputs are specified in the config
#         self.assertEqual(newUpdater.update_database(), True)
