import os
import requests
import datetime as dt


from allauth.socialaccount.models import SocialToken
from .api import ApiCalls
from .date_converter import DateConverter
from datetime import date, datetime, timedelta
from dateutil.parser import parse
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
        'fitness_data' : "",
        'date_count' : "",
        'fitness_count' : "",
        'fitness_total' : "",
        'fitness_avg' : "",
        'error' : [],
    }
    
    endDate = datetime.now().replace(hour=23, minute=59, second=59)
    
    if request.method == 'POST':
        form = request.POST
        # always hate that python does not have switch statements
        if 'getData' in form:   
            # https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format
            
            startDate = is_date(form['startDate'])
            endDate = is_date(form['endDate'])

            
            
            if startDate == "":
                startDate = dt.datetime.now().replace(hour=0, minute=0, second=0)
            if endDate == "":
                endDate = dt.datetime.now().replace(hour=0, minute=0, second=0)

        elif 'thirtyDays' in form:
            startDate = endDate - timedelta(days=29)
            
        elif 'sixtyDays' in form:
            startDate = endDate - timedelta(days=59)
            
        elif 'ninetyDays' in form:
            startDate = endDate - timedelta(days=89)
    else:
        startDate = endDate

   
    if type(startDate) is str:
        startDate = dt.datetime.strptime(startDate, '%a %b %d, %Y')
        
    if type(endDate) is str:
        endDate = dt.datetime.strptime(endDate, '%a %b %d, %Y')

    # check if selected date is greater than 90 days
    startDate.replace(hour=0, minute=0, second=0)
    delta = endDate - startDate
   
    if (delta.days) >= 90:
        endDate = startDate + timedelta(days=89)
        
    reply = api.get_data(startDate, endDate)     

    # error check
    if reply.get("error"):
        fields['error'].append("API Error Token expired, sign out and back in again")
    else:
        fields = json_extract(reply)
        fields['error'] = ""
    
   
    
    #convert dates
    converter = DateConverter()
    for idx, milli_date in enumerate(fields['dates']):
        fields['dates'][idx] = converter.convert_to_date(milli_date)
    
    # setting up all the data to send back to the template
    fields['date_count'] = len(fields["dates"])
    fields['fitness_count'] = len(fields["fitness_data"])
    fields['fitness_total'] = sum(fields['fitness_data'])
    try:
        fields['fitness_avg'] = fields['fitness_total'] / fields['fitness_count']
    except:
        fields['fitness_avg'] = 0
    zippy = zip(fields['dates'], fields['fitness_data']) #combine the two lists
    zippy = list(zippy)
   

    return render(request, 'fitness/fitness.html',{
        "zipped_data" : zippy,
        'd_count' : fields["date_count"],
        's_count' : fields["fitness_count"],
        'total_count' : fields["fitness_total"],
        'average' : fields["fitness_avg"],
        'error' : fields["error"],
    })




def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return string

    except ValueError:
        return ""