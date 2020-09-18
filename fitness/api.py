import os
import requests

from allauth.socialaccount.models import SocialToken
from .date_converter import DateConverter

class ApiCalls():
    """
    This class will make the API queries and return the raw data to the view
    """

    def __init__(self, user):
        """ 
        Constructor  that assigns the access tokena and 
        secret token so that I can refresh the API
        """
        self.access_token = SocialToken.objects.get(account__user=user, account__provider='google')
        self.token_secret = self.access_token.token_secret




    def get_data(self, dataSourceId, startTime, endTime):
        """
        Return JSON of the Fitness API call.  Currently for
        reasons Google only lets you retrieve up to 90 days of activies
        from the API.  

        :param dataSourceId: str the source of the data to be requested
        :param startTime: int the start date of the request in milliseconds
        :param endTime: int the end date of the request in milliseconds
        """
        
        converter = DateConverter()
        start = converter.convert_to_milliseconds(startTime)
        end = converter.convert_to_milliseconds(endTime)
        end = end + 86399000 # makes date to be time set at 23:59:59
        
        url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        
        headers = {
            'Content-type' : 'application/json',
            'Authorization' : 'Bearer ' + str(self.access_token),
        }
        
        # durationMillis is set to one day (24hour period) this 
        # breaks the chunks of data into days
        body = {
            'aggregateBy' : [{'dataSourceId' : dataSourceId }],
            "bucketByTime" : { "durationMillis" : 86400000 },
            "startTimeMillis" : start,
            "endTimeMillis" : end
        }

        response = requests.post(url, json=body, headers=headers)
        
        return response.json()


    
    
    def refresh_token(self):
        """
        This refreshes the API token in hopes to keep it alive 
        however to the best of my abilities the token always
        expires and the User needs to logout and back in again to 
        get a new token to access teh API
        """


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
        
        response = requests.post(url, json=body)
        return response.json()