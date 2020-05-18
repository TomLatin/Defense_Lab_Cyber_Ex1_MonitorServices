import os  # for interacting with the operating system
import psutil  # used to access system details and process utilities,For Windows service library
import subprocess  # For Linux services
import datetime
import time

'''
Is a shell function whose function is to check on which platform our client works and send the parameters to the appropriate function according to the platform. There are 2 functions in which the data can be sent:
1. monitorWin
2. monitorLinux
If the system detects another platform, the customer is notified that the system supports only Windows and Linux platforms.
'''
def monitor(current_os, secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    preparingTheFiles(SERVICE_LIST_FILE, STATUS_LOG_FILE)
    if current_os == "windows":
        monitorWin(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE)
    elif current_os == "linux":
        monitorLinux(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE)
    else:
        print("The system only supports Windows and Linux platforms")

'''
The function gets the file names and checks if they exist if it deletes them and then creates new otherwise it just creates them
'''
def preparingTheFiles(SERVICE_LIST_FILE, STATUS_LOG_FILE):
    if os.path.exists(SERVICE_LIST_FILE):
        os.remove(SERVICE_LIST_FILE)
    if os.path.exists(STATUS_LOG_FILE):
        os.remove(STATUS_LOG_FILE)
    open(SERVICE_LIST_FILE, "w").close()
    open(STATUS_LOG_FILE, "w").close()

'''
The function receives the data from the monitor function and performs one sampling of the services, 
then breaks the number of seconds that the customer defined and then samples the services again on the computer. 
All samples are recorded in the serviceList file.
After the two samples the system compares the 2 samples and if there are any changes it prints the changes on the s
creen and records them in the statusLog file.
input:
1. Seconds between sampling and sampling
2. The serviceList file name
3. The statusLog file name
Output: None
'''
def monitorWin(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    print("Monitor mode is active in Windows platform\n")
    while True:
        dictSample1 = sampleToServiceListWin(open(SERVICE_LIST_FILE, "a"))
        time.sleep(float(secX))
        dictSample2 = sampleToServiceListWin(open(SERVICE_LIST_FILE, "a"))
        sampleToSLogFileWin(STATUS_LOG_FILE, dictSample1, dictSample2)

'''
MonitorWin function auxiliary function, whose function is to register the serviceListFile the sample and return a dictionary
containing the current sample to make it easier to compare the samples.
Input: Open file name
Output: Dictionary
'''
def sampleToServiceListWin(serviceListFile):
    dictToReturn = {}
    # class datetime.datetime give a combination of a date and a time.
    dateWtime = datetime.datetime.now()
    serviceListFile.write("Sampling date and time: {}\n".format(dateWtime))
    for iter in psutil.win_service_iter():
        serviceName = iter.name()
        serviceStatus = iter.status()
        lineToWrite = "{} {}\n".format(serviceName, serviceStatus)
        serviceListFile.write(lineToWrite)
        dictToReturn[serviceName] = serviceStatus
    serviceListFile.write("\n")
    serviceListFile.close()
    return dictToReturn

'''
MonitorWin function auxiliary function, whose function is to log all status changes to the statusLog file and also prints them on the screen.
Input: The file name of statusLog
Output: None
'''
def sampleToSLogFileWin(STATUS_LOG_FILE, dictSample1, dictSample2):
    statusLogFile = open(STATUS_LOG_FILE, "a")
    for key, value in dictSample1.items():
        dateWtime = datetime.datetime.now()
        if key not in dictSample2:
            strToAdd = "Service {} is found at sample 1 but not sample 2. This service probably was uninstalled\n".format(key)
            print(strToAdd)
            statusLogFile.write(strToAdd)
            statusLogFile.flush()
        elif value != dictSample2[key]:
            strToAdd = "{}: Service '{}' changed status from '{}' to '{}'\n".format(dateWtime, key, value, dictSample2[key])
            print(strToAdd)
            statusLogFile.write(strToAdd)
            statusLogFile.flush()
    statusLogFile.close()

'''
Receives the data from the monitor function and performs one sample of the services, then pauses the number of seconds 
defined by the customer and then samples the services again on the computer. All samples are recorded in the serviceList file.
After the two samples the system compares the 2 samples and if there are any changes it prints the changes on the screen
and records them in the statusLog file.
input:
1. Seconds between sampling and sampling
2. The serviceList file name
3. The statusLog file name
Output: None
'''
def monitorLinux(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    print("Monitor mode is active in Linux platform\n")
    while True:
        dictSample1 = sampleToServiceListLinux(open(SERVICE_LIST_FILE, "a"))
        time.sleep(float(secX))
        dictSample2 = sampleToServiceListLinux(open(SERVICE_LIST_FILE, "a"))
        sampleToSLogFileLinux(STATUS_LOG_FILE, dictSample1, dictSample2)

'''
An auxiliary function for the monitorLinux function, whose function is to register to the serviceList file and return a 
dictionary containing the current sample to make it easier to compare the samples.
Input: Open file name
Output: Dictionary
'''
def sampleToServiceListLinux(serviceListFile):
    dictToReturn = {}
    # class datetime.datetime give a combination of a date and a time.
    dateWtime = datetime.datetime.now()
    serviceListFile.write("Sampling date and time: {}\n".format(dateWtime))
    output = subprocess.check_output(["service", "--status-all"])
    for line in output.decode().split('\n'):
        if line[3:4] == '+':
            serviceStatus = "running"
        else:  #line[3:4] == '-'
            serviceStatus = "stopped"
        serviceName = line[8:]
        lineToWrite = "{} {}\n".format(serviceName, serviceStatus)
        serviceListFile.write(lineToWrite)
        dictToReturn[serviceName] = serviceStatus
    serviceListFile.write("\n")
    serviceListFile.close()
    return dictToReturn

'''
The monitorLinux function auxiliary function, whose function is to record all changes that have been made to the statusLog 
file and also prints them on the screen.
Input: filename of statusLog 
Output: None
'''
def sampleToSLogFileLinux(STATUS_LOG_FILE, dictSample1, dictSample2):
    statusLogFile = open(STATUS_LOG_FILE, "w")
    for key, value in dictSample1.items():
        dateWtime = datetime.datetime.now()
        if key not in dictSample2:
            strToAdd = "Service {} is found at sample 1 but not sample 2.\n".format(key)
            print(strToAdd)
            statusLogFile.write(strToAdd)
            statusLogFile.flush()
        elif value != dictSample2[key]:
            status1 = value
            status2 = dictSample2[key]
            strToAdd = "{}: Service '{}' changed status from '{}' to '{}'".format(dateWtime, key, status1, status2)
            print(strToAdd)
            statusLogFile.write(strToAdd)
            statusLogFile.flush()
    statusLogFile.close()

