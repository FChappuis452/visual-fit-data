import os
import requests

from allauth.socialaccount.models import SocialToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .api import ApiCalls
#from oauthlib.oauth2 import BackendApplicationClient



@login_required()
def fitness_home(request):

    api = ApiCalls(request)
    r= api.refresh_token(request)
        
    reply = api.test_call()    

    return render(request, 'fitness/fitness.html',{
        'fitdata' : reply,
        'token' : r
    })

# def refresh_token(token):
#     url = 'https://oauth2.googleapis.com/token'
#     client_secret = os.environ['CLIENT_SECRET']
#     client_id = os.environ['CLIENT_ID']
#     r_token = token.token_secret

#     headers = {
#         'content-type' : 'application/x-www-form-urlencoded',
#     }
    
#     body = f"client_secret={client_secret}&grant_type=refresh_token&refresh_token={r_token}&client_id={client_id}"

    
#     refresh = requests.post(url, data=body)