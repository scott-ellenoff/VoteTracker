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
        response = self.client.post('/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing getting user
        response = self.client.get('/users/'+realUID)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        #setting info
        data = {"name": "L. Ron Hubbard", "district":"60615"}
        response = self.client.put('/users/'+realUID, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed users
        response = self.client.put('/users/'+realUID)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bill(self):
        #testing adding a Bill
        data = {"Description": "this is a description", "status":"P","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.post('/bills/')
        response_body = json.loads(response.content)
        realBID = response_body['BID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing getting Bill
        response = self.client.get('/bills/'+realBID)
        # print(response)
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #changing a Bill status
        data = {"Description": "this is an description", "status":"p","voted_on":"False","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.put('/bills/'+realBID, data)
        # print(response)
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_legislator(self):
        #testing adding legislator
        data = {"fullname" : "Comps Cience", "senator":"false","affiliation":"D","url":"http://www.google.com"}
        response = self.client.post('/legislators/', data, format="json")
        response_body = json.loads(response.content)
        realLID = response_body['LID']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #testing getting legislator
        response = self.client.get('/legislators/'+realLID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #setting info
        data = {"fullname" : "Comps Cience", "senator":"True","affiliation":"R","url":"http://www.google.com"}
        response = self.client.put('/legislators/'+realLID, data)
        # print(response)
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed legislator
        response = self.client.put('/legislators/'+realLID)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote(self):
        data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.post('/bills/')
        response_body = json.loads(response.content)
        realBID = response_body['BID']

        data = {"username": "cc", "name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])

        #testing addinng vote
        data = {"bill":realBID, "legislator":"null", "user":'/users/' + realUID, "vote":"Y"}
        response = self.client.post('/votes/', data)
        print(response)
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
