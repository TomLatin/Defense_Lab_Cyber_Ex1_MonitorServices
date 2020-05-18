import datetime

def validDateWTime(dateWTimeTxt):
    try:
      return datetime.datetime.strptime(dateWTimeTxt, "%Y-%m-%d %H:%M:%S")
    except:
        print("{} : Incorrect data format, it should be YYYY-MM-DD HH:MM:SS".format(dateWTimeTxt))
        return False
