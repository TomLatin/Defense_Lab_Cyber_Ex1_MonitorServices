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

if len(sys.argv) <= 1:
    print("Please add the required information, there are two options:\n 1. Monitor,number of X seconds"
          " \n 2. Manual, first date, first hour, second date, second hour")
    exit()
elif sys.argv[1].lower() == "monitor":

    if len(sys.argv) <= 2:
        print("the required information not supplied, missing number of X seconds")
        exit()
    else:
        current_os = platform.system().lower()
        secX = int(sys.argv[2])
        monitor(current_os, secX, SERVICE_LIST_FILE, STATUS_LOG_FILE)

elif sys.argv[1].lower() == "manual":

    if len(sys.argv) <= 5:
        print("the required information not supplied, missing date or time")
        exit()
    else:
        current_os = platform.system().lower()
        firstDateTxt = sys.argv[2] + " " + sys.argv[3]
        secondDateTxt = sys.argv[4] + " " + sys.argv[5]
        firstDateDT = validDateWTime(firstDateTxt)
        secondDateDT = validDateWTime(secondDateTxt)
        if firstDateDT == False or secondDateDT == False:
            print("The dates were not received in the correct format, the following format:YYYY-MM-DD HH:MM:SS")
            exit()
        manual(firstDateDT, secondDateDT, SERVICE_LIST_FILE)
