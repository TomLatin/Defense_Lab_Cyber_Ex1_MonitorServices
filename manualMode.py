from security import validDateWTime
import os  # for interacting with the operating system
import datetime
import time


def manual(firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE):
  #  if validDateWTime(firstDate, firstHour) and validDateWTime(secondDate, secondHour):
        if os.path.exists(SERVICE_LIST_FILE):
            list1 = findDateWTimeInServiceList(firstDate, firstHour, SERVICE_LIST_FILE)
            list2 = findDateWTimeInServiceList(secondDate, secondHour, SERVICE_LIST_FILE)
            if notAnEmptyList(list1, firstDate + " " + firstHour) and notAnEmptyList(list2, secondDate + " " + secondHour):
                dict1 = listToDict(list1)
                dict2 = listToDict(list2)
                if abs(firstDate + " " + firstHour - secondDate + " " + secondHour) >= 0: #first date is bigger
                  printAllModificationsBetweenTwoDates(dict1, firstDate+" "+firstHour, dict2, secondDate+" "+secondHour)
                else:  #seconde date is bigger
                    printAllModificationsBetweenTwoDates(dict2, secondDate + " " + secondHour, dict1, firstDate + " " + firstHour)
            else:
                exit()
        else:
            print("The system has no information")
            exit()
   # else: #There is a problem with one or both dates
    #    print("The dates were not received in the correct format, the following format:YYYY-MM-DD HH:MM:SS")
     #   exit()

def findDateWTimeInServiceList(date, hour, SERVICE_LIST_FILE):
    listToReturn = []
    hourOfList = ""
    with open(SERVICE_LIST_FILE, "r") as serviceListFile:
        for line in serviceListFile:
            if line[0:24] == "Sampling date and time: " and len(listToReturn) == 0 and line[24:34] == date: #If we found the right date for the first time
                hourOfList = line[35:42]
                if line[35:42] == hour[0:7]: #We will also check if we find the right time, so we will return a list in this iteration
                    nextLine = serviceListFile.__next__()
                    while nextLine[0:24] != "Sampling date and time: ":
                        listToReturn.append(nextLine)
                        nextLine = serviceListFile.__next__()
                    return listToReturn
                else: #Even if we do not find the right time, we will keep the information in case there is no better option
                    nextLine = serviceListFile.__next__()
                    while nextLine[0:24] != "Sampling date and time: ":
                        listToReturn.append(nextLine)
                        nextLine = serviceListFile.__next__()
            if line[0:24] == "Sampling date and time: " and len(listToReturn) != 0 and line[24:34] == date:
                if checkingBetterTime(hour, line, hourOfList):
                        hourOfList = line[35:42]
                        listToReturn = []
                        nextLine = serviceListFile.__next__()
                        while nextLine[0:24] != "Sampling date and time: ":
                            listToReturn.append(nextLine)
                            nextLine = serviceListFile.__next__()
            else:
              print("Something went wrong with date in the file Service List")
              exit()
    return listToReturn

def checkingBetterTime(hour, line, hourOfList):
    hour1 = datetime.datetime.strptime(hour, '%H:%M:%S').time()
    line1 = datetime.datetime.strptime(line[35:42], '%H:%M:%S').time()
    hourOfList1 = datetime.datetime.strptime(hourOfList, '%H:%M:%S').time()
    if abs(hour1 - hourOfList1) > abs(hour1 - line1):
        return True
    else:
        return False


def checkingBetterSec(hour, line, hourOfList):
    return abs(hour[0:1]-hourOfList[0:1]) == abs(hour[0:1] - line[35:36]) and abs(hour[3:4]-hourOfList[3:4]) == abs(hour[0:1]-line[38:39]) and abs(hour[6:7]-hourOfList[6:7]) > abs(hour[6:7]-line[41:42])

def notAnEmptyList(listForCheck, dateWTime):
    if len(listForCheck) == 0:
        print("The system did not find data on the following date and hour:'{}' Or the same date".format(dateWTime))
        return False
    else:
        return True

def listToDict(listForDict):
    dictToReturn = {}
    for line in listForDict:
        listBySplit = line.decode().split(' ')
        dictToReturn[listBySplit[0]] = listBySplit[1]
    return dictToReturn


def printAllModificationsBetweenTwoDates(dict1, firstDateWTime, dict2, secondDateWTime):
    count = 0
    for key, value in dict1.items():
        if key not in dict2:
            strToAdd = "Service '{}' is found at '{}' but not '{}'.\n".format(key, firstDateWTime, secondDateWTime)
            count = count+1
            print(strToAdd)
        elif value != dict2[key]:
            status1 = value
            status2 = dict2[key]
            count = count + 1
            strToAdd = "Service '{}' in the date: '{}' was '{}' and in the date: '{}' it was '{}'.\n'".format(key, firstDateWTime, status1, secondDateWTime, status2)
            print(strToAdd)
    if count == 0:
        print("There were no changes.\n")
    else:
        print("The number of changes that were made are:'{}'".format(count))
