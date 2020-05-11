
import os  # for interacting with the operating system
import psutil  # used to access system details and process utilities,For Windows service library
import subprocess  # For Linux services
import datetime
import time
import logging


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
        sample1 = sampleToServiceListWin(open(SERVICE_LIST_FILE, "w"))
        time.sleep(float(secX))
        sample2 = sampleToServiceListWin(open(SERVICE_LIST_FILE, "w"))
        sampleToSLogFileWin(STATUS_LOG_FILE, sample1, sample2)

def sampleToServiceListWin(ServiceListFile):
    pass


def sampleToSLogFileWin(STATUS_LOG_FILE, sample1, sample2):
    pass


def monitorLinux(secX, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    print("Monitor mode is active in Linux platform\n")
    while True:
        sample1 = sampleToServiceListLinux(open(SERVICE_LIST_FILE, "w"))
        time.sleep(float(secX))
        sample2 = sampleToServiceListLinux(open(SERVICE_LIST_FILE, "w"))
        sampleToSLogFileLinux(STATUS_LOG_FILE, sample1, sample2)

def sampleToServiceListLinux(ServiceListFile):
    pass

def sampleToSLogFileLinux(param):
    pass


