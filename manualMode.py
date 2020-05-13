from security import validDateWTime
import os  # for interacting with the operating system
import datetime
import time


def manual(firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE):
    if validDateWTime(firstDate, firstHour) and validDateWTime(secondDate,secondHour):
        if os.path.exists(SERVICE_LIST_FILE):
            list1 = findDateWTimeInServiceList(firstDate, firstHour, SERVICE_LIST_FILE)
            list2 = findDateWTimeInServiceList(secondDate, secondHour, SERVICE_LIST_FILE)
            printAllModificationsBetweenTwoDates(list1, list2)
        else:
            print("The system has no information")
            exit()
    else: #There is a problem with one or both dates
        print("The dates were not received in the correct format, the following format:YYYY-MM-DD HH:MM:SS")
        exit()

def findDateWTimeInServiceList(date, hour, SERVICE_LIST_FILE):
    listToReturn = []
    hourOfList = ""
    with open(SERVICE_LIST_FILE, "r") as serviceListFile:
        for line in serviceListFile:
            if line[0:24] == "Sampling date and time: " and len(listToReturn) == 0 and line[25:34] == date: #If we found the right date for the first time
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
            elif line[0:24] == "Sampling date and time: " and len(listToReturn) != 0 and line[25:34] == date:
                if abs(hour[0:1]-hourOfList[0:1]) > abs(hour[0:1]-line[35:36]) \
                        or (abs(hour[0:1]-hourOfList[0:1]) == abs(hour[0:1]-line[35:36]) and abs(hour[3:4]-hourOfList[3:4]) > abs(hour[0:1]-line[38:39]))\
                        or (abs(hour[0:1]-hourOfList[0:1]) == abs(hour[0:1]-line[35:36]) and abs(hour[3:4]-hourOfList[3:4]) == abs(hour[0:1]-line[38:39]) and abs(hour[6:7]-hourOfList[6:7]) > abs(hour[6:7]-line[41:42])):
                    listToReturn = []
                    nextLine = serviceListFile.__next__()
                    while nextLine[0:24] != "Sampling date and time: ":
                        listToReturn.append(nextLine)
                        nextLine = serviceListFile.__next__()
            else:
              print("Something went wrong with date in the file Service List")
              exit()
    return listToReturn

def printAllModificationsBetweenTwoDates(list1, list2):
    pass

