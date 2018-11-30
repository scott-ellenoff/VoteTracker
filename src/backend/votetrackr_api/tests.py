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
# class HTTPMethods:
#     def test_post(data, url):
#         return self.client.post(url, data, format="json")


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
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # attempting to add duplicate user 
        response = self.client.post(REGISTER_URL, user_data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body, {'username': ['A user with that username already exists.']})

        user_endpoint = USERS_URL+realUID+'/'

        # testing getting user without properly authenticating
        response = self.client.get(user_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_body, {'detail': ['Authentication credentials were not provided.']})

        user = User.objects.get(id=realUID)
        client = APIClient()
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

        # testing get user on removed users
        response = self.client.get(user_endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bill(self):
        bill_data = {"Description": "this is a description", 
                     "status":"P",
                     "voted_on":"False",
                     "chambers":"S",
                     "session":"2",
                     "url":"http://www.google.com"}


        # testing adding a Bill
        response = self.client.post(BILLS_URL, bill_data)
        response_body = json.loads(response.content)
        realBID = response_body['BID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bill_url = BILLS_URL+realBID+'/'

        # testing getting Bill
        response = self.client.get(bill_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # changing a Bill status
        bill_data = {"Description": "this is a description", 
                     "status":"P",
                     "voted_on":"True",
                     "chambers":"S",
                     "session":"2",
                     "url":"http://www.google.com"}
        response = self.client.put(BILLS_URL, bill_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_legislator(self):
        data = {"fullname" : "Comps Cience", 
                "senator":"False",
                "affiliation":"D",
                "url":"http://www.google.com"}

        #testing adding legislator
        response = self.client.post(LEGISLATOR_URL, data, format="json")
        response_body = json.loads(response.content)
        realLID = response_body['LID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        legislator_url = LEGISLATOR_URL+realLID+'/'

        #testing getting legislator
        response = self.client.get(legislator_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #setting info/changing the info
        data = {"fullname" : "Comps Cience", 
                "senator":"True",
                "affiliation":"R",
                "url":"http://www.google.com"}
        response = self.client.put(legislator_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #deleting a legislator
        response.client.delete(legislator_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed legislator
        response = self.client.get(legislator_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        # #deleting a legislator
        # response.client.delete("/legislators/"+realLID+'/')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # #testing get user on removed legislator
        # response = self.client.delete('http://testserver/legislators/'+realLID+'/')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

        # user = User.objects.create_superuser('admin', 'votetrackr18@gmail.com', 'thisis220') 
        # user.save()
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
        print(response.status_code)
        print(response.content)
        response_body = json.loads(response.content)
        realUID = str(response_body['user']['id'])
        unvoted = response_body['user']['unvoted']
        voted = response_body['user']['voted']

        # Test user created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test user initialized with no voted bills
        self.assertEqual(voted, [])
        # Test user initialized with all unvoted bills
        self.assertEqual(unvoted, [BILLS_URL + bill['BID'] + '/' for bill in bills])

        user = User.objects.get(id=realUID)
        self.client.force_authenticate(user=user)

        vote_data = {'bill': '/api/v1/bills/{}/'.format(bills[0]['BID']), 'vote': 'Y'}
        response = self.client.post(VOTES_USER_URL, vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(USERS_URL + realUID + '/', format='json')
        response_body = json.loads(response.content)
        print(response_body)
        
        # print(response.content)
        # data = {"Description": "this is a description", 
        #         "status":"p",
        #         "voted_on":"True",
        #         "chambers":"S",
        #         "session":"2",
        #         "url":"http://www.google.com"}

        # # test 
        # response = self.client.post('http://testserver/bills/')
        # response_body = json.loads(response.content)
        # realBID = response_body['BID']

        # data = {"username": "cc", "name" : "Comps Cience", "disctict": "10128"}
        # response = self.client.post('http://testserver/users/', data, format="json")
        # response_body = json.loads(response.content)
        # realUID = str(response_body['id'])

        # data = {"fullname" : "Comps Cience", "senator":"False","affiliation":"D","url":"http://www.google.com"}
        # response = self.client.post('http://testserver/legislators/', data, format="json")
        # response_body = json.loads(response.content)
        # realLID = response_body['LID']

        # bill = 'http://localhost:8000/bills/' + realBID + '/'
        # user = 'http://localhost:8000/users/' + realUID + '/'
        # legislator = 'http://localhost:8000/legislators/' + realLID + '/'

        # #testing adding vote with legislator and user
        # data = {"bill": bill, "legislator": legislator, "user": user, "vote":"Y"}
        # response = self.client.post('http://testserver/votes/', data)
        # response_body = json.loads(response.content)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response_body, {'non_field_errors': ['Exactly one of user and legislator should be set.']})

        # #testing adding vote
        # data = {"bill": bill, "user": user, "vote":"Y"}
        # response = self.client.post('http://testserver/votes/', data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # #testing adding duplicate votes
        # response = self.client.post("/votes/", data)
        # response_body = json.loads(response.content)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response_body, {'non_field_errors': ['Vote already exists. Cannot duplicate vote.']})

        # data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        # response = self.client.post('http://testserver/bills/')
        # response_body = json.loads(response.content)
        # realBID = response_body['BID']

        # data = {"username": "cc", "name" : "Comps Cience", "disctict": "10128"}
        # response = self.client.post('http://testserver/users/', data, format="json")
        # response_body = json.loads(response.content)
        # realUID = str(response_body['id'])

        # data = {"fullname" : "Comps Cience", "senator":"False","affiliation":"D","url":"http://www.google.com"}
        # response = self.client.post('http://testserver/legislators/', data, format="json")
        # response_body = json.loads(response.content)
        # realLID = response_body['LID']

        # bill = 'http://localhost:8000/bills/' + realBID + '/'
        # user = 'http://localhost:8000/users/' + realUID + '/'
        # legislator = 'http://localhost:8000/legislators/' + realLID + '/'

        # #testing adding vote with legislator and user
        # data = {"bill": bill, "legislator": legislator, "user": user, "vote":"Y"}
        # response = self.client.post('http://testserver/votes/', data)
        # response_body = json.loads(response.content)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response_body, {'non_field_errors': ['Exactly one of user and legislator should be set.']})

        # #testing adding vote
        # data = {"bill": bill, "user": user, "vote":"Y"}
        # response = self.client.post('http://testserver/votes/', data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # #testing adding duplicate votes
        # response = self.client.post("/votes/", data)
        # response_body = json.loads(response.content)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response_body, {'non_field_errors': ['Vote already exists. Cannot duplicate vote.']})



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

    def test_permissions(self):
        data = {"username": "user1",
                "name" : "First Last", 
                "password": "pa$$w0rd"}

        # Registration
        response = self.client.post('http://testserver/rest-auth/registration', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing getting user without authentication
        response = self.client.get('http://testserver/users/'+realUID+'/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Login with incorrect password
        data = {"username": "user1", "password": "password"}
        response = self.client.post('http://testserver/rest-auth/registration', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Login with correct password
        data["password"] = "pa$$w0rd"
        response = self.client.post('http://testserver/rest-auth/registration', data, format="json")
        response_body = json.loads(response.content)
        token = response_body['key']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Getting user info after authenticated
        self.client.auth = HTTPBasicAuth('user1', 'pa$$w0rd')
        self.client.headers.update({'x-test': 'true'})
        response = self.client.get('http://testserver/users/'+realUID+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Logging out
        response = self.client.post('http://testserver/rest-auth/logout', {}, format="json")
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['detail'], 'Successfully logged out.')

        # Testing getting user info after logout
        response = self.client.get('http://testserver/users/'+realUID+'/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Test suite for an automatic updater
# class UpdaterTests(APITestCase):
#     def test_updater(self):
#         newUpdater = db_updater()

#         # Testing whether the updater can successfully update database with new votes and bills
#         # Returns false if cannot connect to API: either key is old, or API changed the input format - cannot unit test
#         # that since the inputs are specified in the config
#         self.assertEqual(newUpdater.update_database(), True)

#         # Testing pushing notifications to users notifying them that there are new bills they can vote on
#         self.assertEqual(newUpdater.push_notifications(), True)
