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

        #adding user with special character Name
        data = {"username": "cc","name" : "Robert'); DROP TABLE Students;--", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #adding a user with no District
        data = {"username": "cc","name" : "Comps Cience", "disctict": ""}
        response = self.client.post('http://testserver/users/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #attempting to add a duplicate user
        data = {"username": "cc","name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        # print(response)
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #changing a Bill status
        data = {"Description": "this is an description", "status":"P","voted_on":"False","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.put('http://testserver/bills/'+realBID+'/', data)
        # print(response)
        # print(json.loads(response.content))
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
        #add bill
        data = {"Description": "this is a description", "status":"p","voted_on":"True","chambers":"S","session":"2","url":"http://www.google.com"}
        response = self.client.post('http://testserver/bills/')
        response_body = json.loads(response.content)
        realBID = response_body['BID']

        data = {"username": "cc", "name" : "Comps Cience", "disctict": "10128"}
        response = self.client.post('http://testserver/users/', data, format="json")
        response_body = json.loads(response.content)
        realUID = str(response_body['id'])

        #testing adding vote
        data = {"bill":"http://localhost:8000/bills/"+realBID+'/', "legislator":"null", "user":'http://localhost:8000/users/' + realUID+'/', "vote":"Y"}
        response = self.client.post('http://testserver/votes/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #testing adding duplicate votes
        data = data = {"bill":"http://localhost:8000/bills/"+realBID+'/', "legislator":"null", "user":'http://localhost:8000/users/' + realUID+'/', "vote":"Y"}
        response = self.client.post("/votes/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
