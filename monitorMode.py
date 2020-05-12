
import os  # for interacting with the operating system
import psutil  # used to access system details and process utilities,For Windows service library
import subprocess  # For Linux services
import datetime
import time


def monitor(current_os,secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    preparingTheFiles(SERVICE_LIST_FILE, STATUS_LOG_FILE)
    if current_os == "windows":
        monitorWin(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE)
    elif current_os == "linux":
        monitorLinux(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE)

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


def monitorWin(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    print("Monitor mode is active in Windows platform\n")
    while True:
        dictSample1 = sampleToServiceListWin(open(SERVICE_LIST_FILE, "a"))
        time.sleep(float(secX))
        dictSample2 = sampleToServiceListWin(open(SERVICE_LIST_FILE, "a"))
        sampleToSLogFileWin(STATUS_LOG_FILE, dictSample1, dictSample2)


def sampleToServiceListWin(serviceListFile):
    dictToReturn = {}
    # class datetime.datetime give a combination of a date and a time.
    dateWtime = datetime.datetime.now()
    serviceListFile.write("{}\n".format(dateWtime))
    for iter in psutil.win_service_iter():
        serviceName = iter.name()
        serviceStatus = iter.status()
        lineToWrite = "{}{}\n".format(serviceName, serviceStatus)
        serviceListFile.write(lineToWrite)
        dictToReturn[serviceName] = serviceStatus
    serviceListFile.write("\n")
    serviceListFile.close()
    return dictToReturn


def sampleToSLogFileWin(STATUS_LOG_FILE, dictSample1, dictSample2):
    statusLogFile = open(STATUS_LOG_FILE, "a")
    for key, value in dictSample1:
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


def monitorLinux(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    print("Monitor mode is active in Linux platform\n")
    while True:
        dictSample1 = sampleToServiceListLinux(open(SERVICE_LIST_FILE, "a"))
        time.sleep(float(secX))
        dictSample2 = sampleToServiceListLinux(open(SERVICE_LIST_FILE, "a"))
        sampleToSLogFileLinux(STATUS_LOG_FILE, dictSample1, dictSample2)


def sampleToServiceListLinux(serviceListFile):
    dictToReturn = {}
    # class datetime.datetime give a combination of a date and a time.
    dateWtime = datetime.datetime.now()
    serviceListFile.write("{}\n".format(dateWtime))
    output = subprocess.check_output(["service", "--status-all"])
    for line in output.split('\n'):
        serviceName = line[8:]
        serviceStatus = line[3:4]
        lineToWrite = "{} {}\n".format(serviceName, serviceStatus)
        serviceListFile.write(lineToWrite)
        dictToReturn[serviceName] = serviceStatus
    serviceListFile.write("\n")
    serviceListFile.close()
    return dictToReturn


def sampleToSLogFileLinux(STATUS_LOG_FILE, dictSample1, dictSample2):
    statusLogFile = open(STATUS_LOG_FILE, "a")
    for key, value in dictSample1:
        dateWtime = datetime.datetime.now()
        if key not in dictSample2:
            strToAdd = "Service {} is found at sample 1 but not sample 2. This service probably was uninstalled\n".format(
                key)
            print(strToAdd)
            statusLogFile.write(strToAdd)
            statusLogFile.flush()
        elif value != dictSample2[key]:
            status1 = value
            status2 = dictSample2[key]
            if status1 == "+":
                status1 = "running"
            else:
                status1 = "stopped"

            if status2 == "+":
                status2 = "running"
            else:
                status2 = "stopped"
            strToAdd = "{}: Service '{}' changed status from '{}' to '{}'".format(dateWtime, key, status1, status2)
            print(strToAdd)
            statusLogFile.write(strToAdd)
            statusLogFile.flush()
    statusLogFile.close()

