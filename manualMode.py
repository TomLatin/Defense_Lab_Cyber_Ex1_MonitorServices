import os  # for interacting with the operating system
import datetime

'''
input:
1.Date and time (datetime)
2.Date and time (datetime)
3.A string representing the name of the serviceList file

output:
If there were changes between the samples, they would be printed to the screen else Will be printed to the screen there were no changes .
If the date and time were not found in the list service file, we were printed to the screen that we did not find a sample date and time in the list service file.
If the list service file does not exist we printed to the screen that we dont have the information for the system.
'''
def manual(firstDateDT, secondDateDT, SERVICE_LIST_FILE):
        if os.path.exists(SERVICE_LIST_FILE):
            list1 = findDateWTimeInServiceList(firstDateDT, SERVICE_LIST_FILE)
            list2 = findDateWTimeInServiceList(secondDateDT, SERVICE_LIST_FILE)
            if notAnEmptyList(list1, firstDateDT) and notAnEmptyList(list2, secondDateDT):
                dict1 = listTodict(list1)
                dict2 = listTodict(list2)
                zero = datetime.timedelta(0)
                if firstDateDT - secondDateDT >= zero: #first date is bigger
                  printAllModificationsBetweenTwoDates(dict1, firstDateDT, dict2, secondDateDT)
                else:  #seconde date is bigger
                    printAllModificationsBetweenTwoDates(dict2, secondDateDT, dict1, firstDateDT)
            else:
                ''#The customer message was delivered in function:notAnEmptyList
                exit()
        else:
            print("The system has no information")
            exit()
'''
Manual function auxiliary function, its function is to find the date it received in the serviceList file exactly the best
input:
1. Date and time (datetime)
2. A string representing the file name of the serviceList
output:
The function returns a list containing the exact date and time sample of the best second it could find,
if the function did not find the date and time in the file the function returned a empty list.
'''
def findDateWTimeInServiceList(date, SERVICE_LIST_FILE):
    listToReturn = []
    preSec = ""
    with open(SERVICE_LIST_FILE, "r") as serviceListFile:
      try:
        for line in serviceListFile:
                if line[0:23] == "Sampling date and time:" and line[24:34] == str(date.date()) and line[35:37] == str(date.hour) and line[38:40] == str(date.minute):
                    secInThisLine = line[41:43]
                    if secInThisLine == str(date.second):
                        listToReturn = []
                        nextLine = serviceListFile.__next__()
                        while nextLine[0:23] != "Sampling date and time:":
                            listToReturn.append(nextLine)
                            nextLine = serviceListFile.__next__()
                        return listToReturn
                    if not listToReturn: #the list is empty
                       preSec = secInThisLine
                       nextLine = serviceListFile.__next__()
                       while nextLine[0:23] != "Sampling date and time:":
                            listToReturn.append(nextLine)
                            nextLine = serviceListFile.__next__()
                    elif abs(int(date.second)-int(preSec)) > abs(int(date.second)-int(line[41:43])):
                             listToReturn = []
                             preSec = secInThisLine
                             nextLine = serviceListFile.__next__()
                             while nextLine[0:23] != "Sampling date and time:":
                                 listToReturn.append(nextLine)
                                 nextLine = serviceListFile.__next__()

      except StopIteration:
          pass
    return listToReturn

'''
Auxiliary function for the Manual function, its function is to check whether the list returned from 
the findDateWTimeInServiceList function is not empty, if it is empty we let know the client that we did not find a 
sample at this date and time in the serviceList file.
input:
1.List
2. date and time (datetime)
output:
If the list is found to be empty, we will printthat we did not find a 
sample at this date and time in the serviceList file and return False else return True.
'''
def notAnEmptyList(listForCheck, dateWTime):
    if len(listForCheck) == 0:
        print("The system did not find data on the following date and hour:'{}' Or data in that hour".format(dateWTime))
        return False
    else:
        return True

'''
An auxiliary function for the Manual function, its function is to convert the received lists from the 
findDateWTimeInServiceList function to dictionaries in order to make it easier to search for changes between samples.
Input: List
Output: Dictionary
'''
def listTodict(listForDict):
    dictToReturn = {}
    for line in listForDict:
            try:
                serviceName, serviceStatus = line.split(' ')
                dictToReturn[serviceName] = serviceStatus
            except ValueError:
                if len(line) != 1:
                    word = ""
                    serviceName = ""
                    serviceStatus = ""
                    for char in line:
                        if char != ' ':
                            word += char
                        else: #char == ' '
                            if word == "stopped" or word == "running":
                                serviceStatus = word
                            else:
                                serviceName += " "
                                serviceName += word
                    dictToReturn[serviceName] = serviceStatus

    return dictToReturn

'''
An auxiliary function for the Manual function, its function is to print all changes between the 2 samples.
Input: 2 dictionaries and 2 dates (datetime)
Output: Print
'''
def printAllModificationsBetweenTwoDates(dict1, firstDateWTime, dict2, secondDateWTime):
    count = 0
    for key, value in dict1.items():
        if key not in dict2:
            strToAdd = "Service {} is found at {} but not {}\n".format(key, firstDateWTime, secondDateWTime)
            count = count + 1
            print(strToAdd)
        elif value != dict2[key]:
            status1 = value
            status2 = dict2[key]
            count = count + 1
            strToAdd = "Service {} in the date: {} was {} \nand in the date: {} it was {}\n".format(key, firstDateWTime, status1, secondDateWTime, status2)
            print(strToAdd)
    for key, value in dict2.items():
        if key not in dict1:
            strToAdd = "Service {} is found at {} but not {}\n".format(key, firstDateWTime, secondDateWTime)
            count = count + 1
            print(strToAdd)
    if count == 0:
        print("There were no changes.\n")
    else:
        print("The number of changes that were made are:{}".format(count))
