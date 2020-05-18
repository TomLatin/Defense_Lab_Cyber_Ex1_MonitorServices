import datetime

'''
A function whose task is to check whether the user entered us a correct date and time according to the format we work with,
Here is the format: YYYY-MM-DD HH:MM:SS
Input: String type date
Output: If the date in the set format returns datetime object, else false returns.
'''
def validDateWTime(dateWTimeTxt):
    try:
      return datetime.datetime.strptime(dateWTimeTxt, "%Y-%m-%d %H:%M:%S")
    except:
        print("{} : Incorrect data format, it should be YYYY-MM-DD HH:MM:SS".format(dateWTimeTxt))
        return False
