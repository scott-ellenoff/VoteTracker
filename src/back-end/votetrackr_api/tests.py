from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from votetrackr_api.models import User, Bill, Legislator, Vote
# Create your tests here.
import unittest

class UserTests(APITestCase):
    def test_user(self):
        #testing adding user
        data = {"username" : "CompsCience", "name":"Scott Ellenoff", "disctict": "10128"}
        response = self.client.post('/users/', data, format="json")
        realUID = response.UID
        self.assertEqual(response.status_code, status.HTTP_201_Created)

        #testing getting user
        response = self.client.get('/users/'+realUID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #setting info
        data = {"username":"BlahBlah","name": "L. Ron Hubbard", "district":"60615"}
        response = self.client.put('/users/'+realUID, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed users
        response = self.client.put('/users/'+realUID)
        self.assertEqual(response.status_code, status.HTTP_400_Bad_Request)

    def test_bill(self):
        #testing adding a Bill
        data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"asdgfiduhga"}
        response = self.client.post('/bills/')
        realBID = response.BID
        self.assertEqual(response.status_code, status.HTTP_201_Created)

        #testing getting Bill
        response = self.client.get('/bills/'+realBID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #changing a Bill status
        data = {"Description": "this is an description", "status":"p","voted_on":"False","chambers":"S","session":"2","url":"asdgfiduhga"}
        response = self.client.put('/bills/'+realBID, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_legislator(self):
        #testing adding legislator
        data = {"fullname" : "Comps Cience", "senator":"false","affiliation":"D","url":"oasihfd"}
        response = self.client.post('/legislators/', data, format="json")
        realLID = response.LID
        self.assertEqual(response.status_code, status.HTTP_201_Created)

        #testing getting legislator
        response = self.client.get('/legislators/'+realLID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #setting info
        data = {"fullname" : "Comps Cience", "senator":"True","affiliation":"R","url":"oasihfd"}
        response = self.client.put('/legislators/'+realLID, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing get user on removed legislator
        response = self.client.put('/legislators/'+realLID)
        self.assertEqual(response.status_code, status.HTTP_400_Bad_Request)

    def test_vote(self):
        data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"asdgfiduhga"}
        response = self.client.post('/bills/')
        realBID = response.BID
        data = {"name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('/users/', data, format="json")
        realUID = response.UID
        #testing addinng vote
        data = {"bill":realBID, "legislator":"null","user":realUID, "vote":"Y"}
        response = self.client.post('/votes/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
