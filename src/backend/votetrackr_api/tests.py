from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from votetrackr_api.models import User, Bill, Legislator, Vote
from push_notifications.models import APNSDevice, GCMDevice
from votetrackr_api.db_updater import db_updater
# Create your tests here.
import unittest
import json

class UserTests(APITestCase):
    def test_user(self):
        #testing adding user
        data = {"username": "cc","name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #attempting to add a duplicate user
        data = {"username": "cc","name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body, {'username': ['A user with that username already exists.']})
        
        #testing getting user
        response = self.client.get('http://testserver/users/'+realUID+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        #setting info
        data = {"username":"cc","name": "L. Ron Hubbard", "district":"60615"}
        response = self.client.put('http://testserver/users/'+realUID+'/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #removing a user
        response.client.delete("/users/"+realUID+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed users
        response = self.client.get('/users/'+realUID+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bill(self):
        #testing adding a Bill
        data = {"Description": "this is a description", "status":"P","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.post('http://testserver/bills/')
        response_body = json.loads(response.content)
        realBID = response_body['BID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing getting Bill
        response = self.client.get('http://testserver/bills/'+realBID+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #changing a Bill status
        data = {"Description": "this is an description", "status":"P","voted_on":"False","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.put('http://testserver/bills/'+realBID+'/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_legislator(self):
        #testing adding legislator
        data = {"fullname" : "Comps Cience", "senator":"False","affiliation":"D","url":"http://www.google.com"}
        response = self.client.post('http://testserver/legislators/', data, format="json")
        response_body = json.loads(response.content)
        realLID = response_body['LID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing getting legislator
        response = self.client.get('http://testserver/legislators/'+realLID+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #setting info
        data = {"fullname" : "Comps Cience", "senator":"True","affiliation":"R","url":"http://www.google.com"}
        response = self.client.put('http://testserver/legislators/'+realLID+'/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #deleting a legislator
        response.client.delete("/legislators/"+realLID+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed legislator
        response = self.client.delete('http://testserver/legislators/'+realLID+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vote(self):
        data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.post('http://testserver/bills/')
        response_body = json.loads(response.content)
        realBID = response_body['BID']

        data = {"username": "cc", "name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])

        data = {"fullname" : "Comps Cience", "senator":"False","affiliation":"D","url":"http://www.google.com"}
        response = self.client.post('http://testserver/legislators/', data, format="json")
        response_body = json.loads(response.content)
        realLID = response_body['LID']

        bill = 'http://localhost:8000/bills/' + realBID + '/'
        user = 'http://localhost:8000/users/' + realUID + '/'
        legislator = 'http://localhost:8000/legislators/' + realLID + '/'

        #testing adding vote with legislator and user
        data = {"bill": bill, "legislator": legislator, "user": user, "vote":"Y"}
        response = self.client.post('http://testserver/votes/', data)
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body, {'non_field_errors': ['Exactly one of user and legislator should be set.']})

        #testing adding vote
        data = {"bill": bill, "user": user, "vote":"Y"}
        response = self.client.post('http://testserver/votes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing adding duplicate votes
        response = self.client.post("/votes/", data)
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body, {'non_field_errors': ['Vote already exists. Cannot duplicate vote.']})

    def test_match(self):
        #add a legislator
        data = {"fullname" : "Comps Cience", "senator":"False","affiliation":"D","url":"http://www.google.com"}
        response = self.client.post('http://testserver/legislators/', data, format="json")
        response_body = json.loads(response.content)
        realLID = response_body['LID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         #add a user
        data = {"username": "cc","name" : "Scott Ellenoff", "disctict": "10128", "followed" : "Comps Cience"}
        response = self.client.post('http://testserver/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         #add bill
        data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.post('http://testserver/bills/')
        response_body = json.loads(response.content)
        realBID = response_body['BID']
         #add votes
        data = {"bill":"http://localhost:8000/bills/"+realBID+'/', "legislator":"null", "user":'http://localhost:8000/users/' + realUID+'/', "vote":"Y"}
        response = self.client.post('http://testserver/votes/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         data = {"bill":"http://localhost:8000/bills/"+realBID+'/', "legislator":"null", "user":'http://localhost:8000/users/' + realLID+'/', "vote":"Y"}
        response = self.client.post('http://testserver/votes/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         #test matching
        response = self.client.get('http://testserver/users/'+realUID+'/')
        response_body = json.loads(response.content)
        matched = response_body['matched']
        self.assertEqual(matched, {realLID:"1.00"}})
         #attempting to follow a fake legislators
        data = {"username":"cc","name": "L. Ron Hubbard", "district":"60615", "followed":"Json Bourne"}
        response = self.client.put('http://testserver/users/'+realUID+'/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permissions(self):
        # Registration
        data = {"username": "user1","name" : "First Last", "password": "pa$$w0rd"}
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



class PushNotificationsTests(unittest.TestCase):

    # Spoke with Yuxi on Monday --- these tests will fail due to the fact that we currently don't have
    # Google Cloud Messaging or Apple Push Notification System tokens set up yet. Thus, it will throw an error
    # when it tries to define the "device" variable since we don't have users that are GCM or APNS objects yet.
    # In my conversation with Yuxi he concluded that this was acceptable for Iteration 4a. This will be set up 
    # for iteration 4b.
    def test_push_android(self):
        # Android push notifications

        gcm_reg_id = "0"
        the_user = "user"
        device = GCMDevice.objects.create(registration_id=gcm_reg_id, cloud_message_type="FCM", user=the_user)

        # simple text message
        response = device.send_message("New Bill")
        self.assertEqual(response[0].getcode(), 200)

        # extra payload message
        response = device.send_message("Extra message", extra={"title": "New Bill", "icon": "icon"})
        self.assertEqual(response[0].getcode(), 200)

        # extra data message
        response = device.send_message("Message with data", extra={"other": "Bill Content", "misc": "Bill Data"})
        self.assertEqual(response[0].getcode(), 200)

        # limited life message
        response = device.send_message("This is a message", time_to_live=3600)
        self.assertEqual(response[0].getcode(), 200)

        # fail to create device with bad userID
        gcm_reg_id = "-1"
        the_user = "baduser"
        device = GCMDevice.objects.create(registration_id=gcm_reg_id, cloud_message_type="FCM", user=the_user)
        self.assertEqual(device, None)


    def test_push_IOS(self):
        # iOS push notifications

        apns_token = 1
        device = APNSDevice.objects.get(registration_id=apns_token)

        # simple text message
        response = device.send_message("New Bill")
        self.assertEqual(response[0].getcode(), 200)

        # just badge, no alert
        response = device.send_message(None, badge=5)
        self.assertEqual(response[0].getcode(), 200)

        # notification with title and body
        response = device.send_message(message={"title" : "New Bill", "body" : "Bill 101: This is a Bill Title"})
        self.assertEqual(response[0].getcode(), 200)

        # fail to create device with bad userID
        apns_token = -1
        device = APNSDevice.objects.get(registration_id=apns_token)
        self.assertEqual(device, None)


# Test suite for an automatic updater
class UpdaterTests(APITestCase):
    def test_updater(self):
        newUpdater = db_updater()

        # Testing whether the updater can successfully update database with new votes and bills
        # Returns false if cannot connect to API: either key is old, or API changed the input format - cannot unit test
        # that since the inputs are specified in the config
        self.assertEqual(newUpdater.update_database(), True)

        # Testing pushing notifications to users notifying them that there are new bills they can vote on
        self.assertEqual(newUpdater.push_notifications(), True)

