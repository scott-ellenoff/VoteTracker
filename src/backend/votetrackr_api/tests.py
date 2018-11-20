from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from votetrackr_api.models import User, Bill, Legislator, Vote
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

        #adding user with special character Name
        data = {"username": "cc","name" : "Robert'); DROP TABLE Students;--", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #adding a user with no District
        data = {"username": "cc","name" : "Comps Cience", "disctict": ""}
        response = self.client.post('http://testserver/users/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
