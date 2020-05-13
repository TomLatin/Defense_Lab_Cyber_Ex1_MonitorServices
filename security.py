import datetime
import time

def validDateWTime(date, hour):
    return datetime.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S")
