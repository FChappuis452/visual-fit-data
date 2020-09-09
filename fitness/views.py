import os
import requests
import datetime as dt


from allauth.socialaccount.models import SocialToken
from .api import ApiCalls
from .date_converter import DateConverter
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .extract import *

INVALID_DATE = "Invalid date"


@login_required()
def fitness_home(request):
    #Init API 
    api = ApiCalls(request)
    api.refresh_token(request)
    
    reply = ""
    # Init the django fields
    fields = {
        'dates' : "",
        'fitness_info' : "",
        'date_count' : "",
        'fitness_count' : "",
    }
    
    endDate = datetime.now().replace(hour=0, minute=0, second=0)
    
    if request.method == 'POST':
        form = request.POST
        # always hate that python does not have switch statements
        if 'getData' in form:   
            startDate = form['startDate']
            endDate = form['endDate']

            if startDate == "":
                startDate = dt.datetime.now().replace(hour=0, minute=0, second=0)
            if endDate == "":
                endDate = dt.datetime.now().replace(hour=0, minute=0, second=0)

        elif 'fourWeeks' in form:
            startDate = endDate - timedelta(weeks=4)
            
        elif 'threeMonth' in form:
            startDate = endDate + relativedelta(months=-3)
            
        elif 'sixMonth' in form:
            startDate = endDate + relativedelta(months=-6)
            
        elif 'twelveMonth' in form:
            startDate = endDate + relativedelta(months=-12)
            
    else:
        startDate = endDate

   
    if type(startDate) is str:
        startDate = dt.datetime.strptime(startDate, '%a %b %d, %Y')
        
    if type(endDate) is str:
        endDate = dt.datetime.strptime(endDate, '%a %b %d, %Y')
        
    reply = api.get_data(startDate, endDate)            

    fields = json_extract(reply)
    
   
    fields['date_count'] = len(fields["dates"])
    fields['fitness_count'] = len(fields["fitness_data"])

    #convert dates
    converter = DateConverter()
    for idx, milli_date in enumerate(fields['dates']):
        fields['dates'][idx] = converter.convert_to_date(milli_date)
    
    
       

    return render(request, 'fitness/fitness.html',{
        'dates' : fields["dates"],
        'steps' : fields["fitness_data"],
        'd_count' : fields["date_count"],
        's_count' : fields["fitness_count"],
        
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