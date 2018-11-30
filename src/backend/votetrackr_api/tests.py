from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from votetrackr_api.models import User, Bill, Legislator, Vote
# from push_notifications.models import APNSDevice, GCMDevice
# from votetrackr_api.db_updater import db_updater
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

        for bill in bills:
            response = self.client.post(BILLS_URL, bill)
            # response_body = json.loads(response.content)
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

        user = User.objects.get(id=realUID)
        self.client.force_authenticate(user=user)


        unvoted = response_body['user']['unvoted']
        voted = response_body['user']['voted']
        self.assertEqual(unvoted, [BILLS_URL + '{}/'.format(bill['BID']) for bill in bills])
        self.assertEqual(voted, [])

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

    # def test_permissions(self):
    #     data = {"username": "user1",
    #             "name" : "First Last", 
    #             "password": "pa$$w0rd"}

    #     # Registrate the user we'll test
    #     response = self.client.post(REGISTER_URL, data, format="json")
    #     response_body = json.loads(response.content)
    #     realUID1 = str(response_body['user']['id'])
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     other_user = {"username": "user2",
    #                   "name" : "Firstname Lastname", 
    #                   "password": "s0ftwar3"}

    #     # Registrate a second user to test against
    #     response = self.client.post(REGISTER_URL, data, format="json")
    #     response_body = json.loads(response.content)
    #     realUID2 = str(response_body['id'])
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     user1_url = USERS_URL+realUID1+'/'
    #     user2_url = USERS_URL+realUID2+'/'

    #     #testing getting user without authentication
    #     response = self.client.get(user1_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # # login to authenticate
    #     # client = APIClient()
    #     # client.login(username='user1', password='pa$$w0rd')

    #     # Login with incorrect password
    #     data = {"username": "user1", "password": "password"}
    #     response = self.client.post(LOGIN_URL, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #     # login correctly
    #     client = APIClient()
    #     client.login(username='user1', password='pa$$w0rd')

    #     # Getting user info after authenticated
    #     response = self.client.get(user1_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Getting the other user info after authenticated
    #     response = self.client.get(user2_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # Getting user list view after authenticated
    #     response = self.client.get(USERS_URL)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Logging out
    #     client.logout()

    #     # Testing getting user info after logout
    #     response = self.client.get(user1_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # Getting user list view after logout
    #     response = self.client.get(USERS_URL)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # # Registration
    #     # response = self.client.post('http://testserver/rest-auth/registration', data, format="json")
    #     # response_body = json.loads(response.content)
    #     # realUID = str(response_body['id'])
    #     # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # #testing getting user without authentication
    #     # response = self.client.get('http://testserver/users/'+realUID+'/')
    #     # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # # Login with incorrect password
    #     # data = {"username": "user1", "password": "password"}
    #     # response = self.client.post('http://testserver/rest-auth/registration', data, format="json")
    #     # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     # # Login with correct password
    #     # data["password"] = "pa$$w0rd"
    #     # response = self.client.post('http://testserver/rest-auth/registration', data, format="json")
    #     # response_body = json.loads(response.content)
    #     # token = response_body['key']
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # # Getting user info after authenticated
    #     # self.client.auth = HTTPBasicAuth('user1', 'pa$$w0rd')
    #     # self.client.headers.update({'x-test': 'true'})
    #     # response = self.client.get('http://testserver/users/'+realUID+'/')
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # # Logging out
    #     # response = self.client.post('http://testserver/rest-auth/logout', {}, format="json")
    #     # response_body = json.loads(response.content)
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(response_body['detail'], 'Successfully logged out.')

    #     # # Testing getting user info after logout
    #     # response = self.client.get('http://testserver/users/'+realUID+'/')
    #     # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # def test_match(self):
    #     #add a legislator
    #     data = {"fullname" : "Comps Cience", "senator":"False","affiliation":"Democrat","url":"http://www.google.com"}
    #     response = self.client.post(base + 'legislators/', data, format="json")
    #     response_body = json.loads(response.content)
    #     realLID = response_body['LID']
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #      #add a user
    #     data = {"username": "cc","name" : "Scott Ellenoff", "disctict": "10128", "followed": ['/api/v1/legislators/' + realLID + '/']}
    #     response = self.client.post(base + 'users/', data, format="json")
    #     response_body = json.loads(response.content)
    #     print(response.content)
    #     realUID = str(response_body['id'])
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #      #add bill
    #     data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
    #     response = self.client.post(base + 'bills/')
    #     response_body = json.loads(response.content)
    #     realBID = response_body['BID']
    #      #add votes
    #     data = {'bill': base + 'bills/'+realBID+'/', "legislator":"null", "user": base + 'users/' + realUID+'/', "vote":"Y"}
    #     response = self.client.post(base + 'votes/', data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     data = {'bill': base + 'bills/' + realBID + '/', 'legislator':"null", "user": base + 'users/' + realLID+'/', "vote":"Y"}
    #     response = self.client.post(base + 'votes/', data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #      #test matching
    #     response = self.client.get(base + 'users/'+realUID+'/')
    #     response_body = json.loads(response.content)
    #     MID = response_body['matched']
    #     response = self.client.get(base + 'match/'+MID+'/')
    #     response_body = json.loads(response.content)
    #     matchPercentage = response_body['matchPercentage']
    #     self.assertEqual(matchPercentage, 1.0)
    #      #attempting to follow a fake legislators
    #     data = {"username":"cc","name": "L. Ron Hubbard", "district":"60615", "followed":"Json Bourne"}
    #     response = self.client.put(base + 'users/'+realUID+'/', data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

   
# class UpdaterTests(APITestCase):
#     def test_updater(self):
#         newUpdater = db_updater()

#         # Testing whether the updater can successfully update database with new votes and bills
#         # Returns false if cannot connect to API: either key is old, or API changed the input format - cannot unit test
#         # that since the inputs are specified in the config
#         self.assertEqual(newUpdater.update_database(), True)

#         # Testing pushing notifications to users notifying them that there are new bills they can vote on
#         self.assertEqual(newUpdater.push_notifications(), True)
