import os
import requests

from allauth.socialaccount.models import SocialToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

#from oauthlib.oauth2 import BackendApplicationClient



@login_required()
def fitness_home(request):
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
    print(reply)

    return render(request, 'fitness/fitness.html',{
        'fitdata' : reply,
        'token' : access_token
    })

def refresh_token(token):
    url = 'https://oauth2.googleapis.com/token'
    client_secret = os.environ['CLIENT_SECRET']
    client_id = os.environ['CLIENT_ID']
    r_token = token.token_secret

    headers = {
        'content-type' : 'application/x-www-form-urlencoded',
    }
    
    body = f"client_secret={client_secret}&grant_type=refresh_token&refresh_token={r_token}&client_id={client_id}"

    
    refresh = requests.post(url, data=body)