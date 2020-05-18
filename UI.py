from manualMode import manual
from monitorMode import monitor
from security import validDateWTime
import platform  # provides system information like on which the program is being currently executed
import sys

SERVICE_LIST_FILE = "serviceList.log"
STATUS_LOG_FILE = "statusLog.log"

'''
The function receives from the user if they want a monitor mode service and if it is expected that the user will
also provide the number of seconds in which they want the mode to sample all services running.
Or if they want a manual mode service and if so we expect the user to provide a 
first date and first hour and a second date and second hour.
on condition we get all the information we want, we pass the information to the relevant function in the relevant
department otherwise we will print an error and close the program.
'''
mode = 0
while mode != 3:
    mode = int(input("Choose mode: \n    1 - manual\n    2 - monitor\n    3 - exit\n"))
    if mode == 1:
        flag = True
        try:
            d1, t1, d2, t2 = input("enter 2 dates and times: ").split()
            firstDateTxt = d1 + " " + t1
            secondDateTxt = d2 + " " + t2
        except ValueError:
            print("not enough values, please enter YYYY-MM-DD HH:MM:SS YYYY-MM-DD HH:MM:SS\n")
            flag = False
        if flag:
            firstDateDT = validDateWTime(firstDateTxt)
            secondDateDT = validDateWTime(secondDateTxt)
            if firstDateDT == False or secondDateDT == False:
              print("The dates were not received in the correct format, the following format:YYYY-MM-DD HH:MM:SS\n")
              flag = False
        if flag:
             manual(firstDateDT, secondDateDT, SERVICE_LIST_FILE)
    elif mode == 2:
        flag = True
        current_os = platform.system().lower()
        try:
          secX = int(input("enter secounds: \n"))
        except ValueError:
            print("The resulting input is not an integer\n")
            flag = False
        if flag:
            monitor(current_os, secX, SERVICE_LIST_FILE, STATUS_LOG_FILE)