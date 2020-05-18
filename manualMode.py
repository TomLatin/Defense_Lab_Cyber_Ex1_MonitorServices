import os  # for interacting with the operating system
from security import validDateWTime
import datetime
import time

def manual(firstDateDT, secondDateDT, SERVICE_LIST_FILE):
        if os.path.exists(SERVICE_LIST_FILE):
            list1 = findDateWTimeInServiceList(firstDateDT, SERVICE_LIST_FILE)
            list2 = findDateWTimeInServiceList(secondDateDT, SERVICE_LIST_FILE)
            if notAnEmptyList(list1, firstDateDT) and notAnEmptyList(list2, secondDateDT):
                dict1 = listToDict(list1)
                dict2 = listToDict(list2)
                zero = datetime.timedelta(0)
                if abs(firstDateDT - secondDateDT) >= zero: #first date is bigger
                  printAllModificationsBetweenTwoDates(dict1, firstDateDT, dict2, secondDateDT)
                else:  #seconde date is bigger
                    printAllModificationsBetweenTwoDates(dict2, secondDateDT, dict1, firstDateDT)
            else:
                ''#The customer message was delivered in function:notAnEmptyList
                exit()
        else:
            print("The system has no information")
            exit()

def findDateWTimeInServiceList(date, SERVICE_LIST_FILE):
    listToReturn = []
    hourOfList = ""
    c=0
    with open(SERVICE_LIST_FILE, "r") as serviceListFile:
        try:
            for line in serviceListFile:
                if line[0:24] == "Sampling date and time: " and len(listToReturn) == 0 and line[24:34] == str(date.date()) and line[35:37] == str(date.hour):
                    print("in111111111111111111111111111111111")
                    hourOfList = line[24:43]
                    print("hourOfList:{}".format(hourOfList))
                    if line[35:43] == str(date):  # We will also check if we find the right time, so we will return a list in this iteration
                        nextLine = serviceListFile.__next__()
                        while nextLine[0:24] != "Sampling date and time: ":
                            listToReturn.append(nextLine)
                            nextLine = serviceListFile.__next__()
                        #print("{}\n".format(listToReturn))
                        #print("*********************************")
                        return listToReturn
                    else:  # Even if we do not find the right time, we will keep the information in case there is no better option
                        nextLine = serviceListFile.__next__()
                        while nextLine[0:24] != "Sampling date and time: ":
                            listToReturn.append(nextLine)
                            nextLine = serviceListFile.__next__()
                            print("*********************************")
                        print("{}\n".format(listToReturn))
                print("line:{}".format(line))
                if line[0:24] == "Sampling date and time: " and len(listToReturn) != 0 and line[24:34] == str(date.date()) and int(line[35:37]) == date.hour:
                    print("in22222222222222222222222")
                    print("line[24:43]:{}".format(line[24:43]))
                    if checkingBetterTime(date, line[24:43], hourOfList):
                        c=c+1
                        print(c)
                        hourOfList = line[24:43]
                        listToReturn = []
                        nextLine = serviceListFile.__next__()
                        while nextLine[0:24] != "Sampling date and time: ":
                            listToReturn.append(nextLine)
                            nextLine = serviceListFile.__next__()
                            #print("{}\n".format(listToReturn))
                            #print("*********************************")
        except StopIteration:
            pass
    return listToReturn


def checkingBetterTime(date, line, hourOfList):
    fileDate = validDateWTime(line)
    preDate = validDateWTime(hourOfList)
    print("date:{}".format(date))
    print("fileDate:{}".format(fileDate))
    print("preDate:{}".format(preDate))
    print("abs(date - preDate):{}".format(abs(date - preDate)))
    print("abs(date - fileDate):{}".format(abs(date - fileDate)))
    if abs(date - preDate) > abs(date - fileDate):
        print("true")
        return True
    else:
        print("false")
        return False

def notAnEmptyList(listForCheck, dateWTime):
    if len(listForCheck) == 0:
        print("The system did not find data on the following date and hour:'{}' Or data in that hour".format(dateWTime))
        return False
    else:
        return True

def listToDict(listForDict):
    print("listForDict:{}".format(listForDict))
    dictToReturn = {}
   # print(listForDict)
    try:
        for line in listForDict:
            print(len(line))
            if len(line) != 1:
                 serviceName, serviceStatus = line.split(' ')
                 print("serviceName:{} , serviceStatus:{}".format(serviceName, serviceStatus))
                 dictToReturn[serviceName] = serviceStatus
        print(dictToReturn)
        return dictToReturn
    except ValueError:
        print(line)


def printAllModificationsBetweenTwoDates(dict1, firstDateWTime, dict2, secondDateWTime):
    print(dict1)
    print(dict2)
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
