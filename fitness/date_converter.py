import datetime
import time 
import math

class DateConverter():
    """
    This class will convert dates to milliseconds and vice versa
    https://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
    https://www.programiz.com/python-programming/datetime/timestamp-datetime
    """

    one_day = 86400000 # milliseconds in one day

    def convert_to_milliseconds(self, date_to_convert):
        """
        Takes a date object and returns a converted milliseconds
        :param date_to_convert: str date object to be converted
        """        

        milliseconds = date_to_convert.timestamp() * 1000
        
        return math.trunc(milliseconds) #removes any decimals from the convertion




    def convert_to_date(self, milliseconds):
        """
        Returns a date object from milliseconds
        :param milliseconds: int the number to be converted into a date object
        """

        milli = int(milliseconds)
        milli = milli / 1000.0

        # format codes can be found here https://www.w3schools.com/python/python_datetime.asp
        dt_object = datetime.datetime.fromtimestamp(milli).strftime("%a %b %d, %Y")
        return dt_object