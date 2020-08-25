![image](https://user-images.githubusercontent.com/57855070/91161598-9de8f780-e6d3-11ea-952d-499cb228c497.png)

In this project we have built a tool that will monitor our running services in the system, and report on changes that may be critical for us as SOC people. The tool is a cross platform - that is, run on both the Windows operating system and the Linux operating system. Please use Linux in the Ubuntu distribution.

The tool is intended for testing for a single server and not for a network, which means that the tool will monitor the services running on the same computer running the software.

### Our tool will have several modes:
* #### Monitor mode:
  For the X time set by the user, the program samples every X time all the services running on the computer, and shows whether a change from the previous sample was observed. That   is, is there a service that is no longer running, or is there a service
  New running in the system. Any change that has taken place should alert the user to the interface.

* #### Manual mode: 
  In this mode we would like to use the serviceList file to load 2 samples from different time frames and make a comparison. The program will get a date and time for 2 events,       load the 2 samples from the file, and display changes similar to the monitor state (a new process created in the latest sample, a process that no longer runs 
  in the more recent sample, etc.)

* #### UI: 
  To allow the user to navigate comfortably between modes,We created a UI menu for the tool. 

#### For more information please read the Wiki.
