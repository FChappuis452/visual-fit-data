import os
import requests


from allauth.socialaccount.models import SocialToken
from .api import ApiCalls
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .extract import *

INVALID_DATE = "Invalid date"


@login_required()
def fitness_home(request):
    api = ApiCalls(request)
    api.refresh_token(request)
    reply = ""
    dates = ""
    steps = 0
    date_count = 0
    step_count = 0
    m = "not assigned"
    if request.method == 'POST':
        form = request.POST
        today = datetime.now()
        # always hate that python does not have switch statements
        if 'getData' in form:
            if form['startDate'] == '' or form['endDate'] == '':
                reply = INVALID_DATE
            else:    
                reply = api.get_data(form['startDate'], form['endDate'])
                # reply = json_extract(reply, 'intVal')
            
            m = f"{form['startDate']} {form['endDate']}'"
            
        elif 'fourWeeks' in form:
            endDate = today - timedelta(weeks=4)
            reply = api.get_data(endDate, today)
            m = f"{today}, {endDate}"
        elif 'threeMonth' in form:
            endDate = today + relativedelta(months=-3)
            reply = api.get_data(endDate, today)
            m = f"{today}, {endDate}"
        elif 'sixMonth' in form:
            endDate = today + relativedelta(months=-6)
            reply = api.get_data(endDate, today)
            m = f"{today}, {endDate}"
        elif 'twelveMonth' in form:
            endDate = today + relativedelta(months=-12)
            reply = api.get_data(endDate, today)
            m = f"{today}, {endDate}"
        else:
            reply = INVALID_DATE
    else:
        m = "else clause"

    if reply != "" and reply != INVALID_DATE:
        dates = json_extract(reply, 'startTimeMillis')
        steps = json_extract(reply, 'intVal')
        date_count = len(dates)
        step_count = len(steps)
    
    
       

    return render(request, 'fitness/fitness.html',{
        'dates' : dates,
        'steps' : steps,
        'd_count' : date_count,
        's_count' : step_count,
        'date_query' : m
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