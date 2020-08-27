"""
This class will convert dates to milliseconds and vice versa
https://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
https://www.programiz.com/python-programming/datetime/timestamp-datetime

"""
import datetime
import time 
import math



class DateConverter():

    one_day = 86400000 # milliseconds in one day

    def convert_to_milliseconds(self, date_to_convert):
        
        if type(date_to_convert) is str:
            converted_date = datetime.datetime.strptime(date_to_convert, '%a %b %d, %Y')
        else:
            converted_date = date_to_convert
        milliseconds = converted_date.timestamp() * 1000
        print (milliseconds)
        print (math.trunc(milliseconds)) 
        return math.trunc(milliseconds)

    def convert_to_date(self, milliseconds):
        dt_object = datetime.fromtimestamp(milliseconds)
        return dt_object
