"""
This class will make the API queries and return the raw data to the view
"""


"""
access_token = SocialToken.objects.get(account__user=request.user, account__provider='google')
    refresh_token(access_token)

    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
    headers = {
        'Content-type' : 'application/json',
        'Authorization' : 'Bearer ' + str(access_token),
    }
    
    body = {
        'aggregateBy' : [{'dataSourceId' : 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'}],
        "bucketByTime" : { "durationMillis" : 86400000 },
        "startTimeMillis" : 1593921600000,
        "endTimeMillis" : 1594094399000
    }

    response = requests.post(url, json=body, headers=headers)
    reply = response.json()
    

"""
import os
import requests

from allauth.socialaccount.models import SocialToken
from .date_converter import DateConverter

class ApiCalls():

    def __init__(self, request):
        self.access_token = SocialToken.objects.get(account__user=request.user, account__provider='google')
        self.token_secret = self.access_token.token_secret
    

    def get_data(self, startTime, endTime):
        converter = DateConverter()
        start = converter.convert_to_milliseconds(startTime)
        end = converter.convert_to_milliseconds(endTime)

        if start == end:
            end = end + 86399000
        

        url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        headers = {
            'Content-type' : 'application/json',
            'Authorization' : 'Bearer ' + str(self.access_token),
        }
        
        body = {
            'aggregateBy' : [{'dataSourceId' : 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'}],
            "bucketByTime" : { "durationMillis" : 86400000 },
            "startTimeMillis" : start,
            "endTimeMillis" : end
        }

        response = requests.post(url, json=body, headers=headers)
        print(response.json())
        return response.json()


    
    
    def refresh_token(self, request):
        client_secret = os.environ['CLIENT_SECRET']
        client_id = os.environ['CLIENT_ID']
        url = 'https://oauth2.googleapis.com/token'

        headers = {
            'content-type' : 'application/x-www-form-urlencoded',
        }
        
        body = {
            'client_secret' : client_secret,
            'grant_type' : 'refresh_token',
            'refresh_token' : self.token_secret,
            'client_id' : client_id
        }
            # f"client_secret={client_secret}&grant_type=refresh_token&refresh_token={self.token_secret}&client_id={client_id}"
        
        
        response = requests.post(url, json=body)
        return response.json()
