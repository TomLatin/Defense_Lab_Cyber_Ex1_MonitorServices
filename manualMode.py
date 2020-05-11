import platform  # provides system information like on which the program is being currently executed
import os  # for interacting with the operating system
import psutil  # used to access system details and process utilities,For Windows service library
import subprocess  # For Linux services
import datetime
import time

def manual(current_os, firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    if current_os == "windows":
        manualWin(firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE, STATUS_LOG_FILE)
    elif current_os == "linux":
        manualLinux(firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE, STATUS_LOG_FILE)

def manualWin(firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    pass
def manualLinux(firstDate, firstHour, secondDate, secondHour, SERVICE_LIST_FILE, STATUS_LOG_FILE):
    pass

