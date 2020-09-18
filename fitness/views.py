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
from django.http import HttpResponse
from .extract import *


@login_required
def steps(request):
    """
    Returns the rendering for the API calls mades for steps requests
    """

    path = 'fitness/steps.html'
    if not request.POST:
        return render(request, path)
    else:
        form = request.POST
        user = request.user
        fields = form_direct(form, user, "steps")

        zippy = zip(fields['dates'], fields['fitness_data']) #combine the two lists
        zippy = list(zippy)
        
        return render(request, path,{
            "zipped_data" : zippy,
            'd_count' : fields["date_count"],
            's_count' : fields["fitness_count"],
            'total_count' : fields["fitness_total"],
            'average' : fields["fitness_avg"],
            'error' : fields["error"],   
        })




@login_required
def calories(request):
    """
    Returns the rendering for the API calls mades for calorie requests
    """

    path = 'fitness/calories.html'
    if not request.POST:
        return render(request, path)
    else:
        form = request.POST
        user = request.user
        fields = form_direct(form, user, "calories")
        zippy = zip(fields['dates'], fields['fitness_data']) #combine the two lists
        zippy = list(zippy)
        
        return render(request, path,{
            "zipped_data" : zippy,
            'd_count' : fields["date_count"],
            's_count' : fields["fitness_count"],
            'total_count' : fields["fitness_total"],
            'average' : fields["fitness_avg"],
            'error' : fields["error"],   
        })




def form_direct(form, user, page_render):
    """
    Returns dictionary of formatted API data
    :param form: POST data from the form request
    :param user: The user that made the form request
    :param page_render: str what type of data to retrieve
    """

    if page_render == "steps":
        datasourceId = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
        fields = form_control(form, user, datasourceId, page_render)
        return fields

    elif page_render == "calories":
        datasourceId = 'derived:com.google.calories.expended:com.google.android.gms:from_activities'
        fields = form_control(form, user, datasourceId, page_render)
        return fields




def form_control(form, user, datasourceId, page):
    """
    Return the dictionary after making the API call

    :param form: The form data from request.POST
    :param user: The user making the request
    :param datasourceId: str The Id of the data to be retrieved
    :param page: str the type of data being retrieved
    """
    #Init API
    api = ApiCalls(user)
    api.refresh_token()

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

    # Work through which button was pushed on the form
    if 'getData' in form:   
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
        
    reply = api.get_data(datasourceId, startDate, endDate)     
    
    # error check
    if reply.get("error"):
        fields['error'].append("API Error Token expired, sign out and back in again")
    else:
        fields = json_extract(reply, page)
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

    return fields




def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return string

    except ValueError:
        return ""