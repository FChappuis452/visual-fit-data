import os
import requests

from allauth.socialaccount.models import SocialToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from oauthlib.oauth2 import BackendApplicationClient



@login_required()
def fitness_home(request):
    access_token = SocialToken.objects.get(account__user=request.user, account__provider='google')
    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
    headers = {
        'Content-type' : 'application/json',
        'Authorization' : 'Bearer ' + str(access_token),
    }
    
    body = {
        'aggregateBy' : [{'dataSourceId' : 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'}],
        "bucketByTime" : { "durationMillis" : 86400000 },
        "startTimeMillis" : 1593921600000,
        "endTimeMillis" : 1594007999000
    }

    response = requests.post(url, json=body, headers=headers)
    reply = response.json()
    print(reply)

    return render(request, 'fitness/fitness.html',{
        'fitdata' : reply,
    })
