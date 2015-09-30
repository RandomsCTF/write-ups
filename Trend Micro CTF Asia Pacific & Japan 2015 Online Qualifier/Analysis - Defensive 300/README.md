# Analysis - Defensive 300

## Problem

This is a REAL backdoor network traffic!

Tracing hacker's footprint to find the key!

Hint:

Poison Ivy / admin

[net.pcap](net.pcap)

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

Essentially, this task is just a lot of googling and documentation searching, nothing too technical. "Poison Ivy / admin" hints us to the kind of backdoor used here—`W32/PoisonIvy`—and also the password `admin` (which is a default password for Poison Ivy anyway, so that wasn't really necessary).

A framework that can analyze Poison Ivy traffic (as well as other interesting things) is [ChopShop](https://github.com/MITRECND/chopshop), and the biggest pain in the ass of this challenge was to make the tool and all its dependencies compile and run on Ubuntu.

Let's analyze the stream now:
```
$ ./chopshop 'poisonivy_23x' -f ../net.pcap
Warning Legacy Module poisonivy_23x!
Starting ChopShop
Initializing Modules ...
  Initializing module 'poisonivy_23x'
Running Modules ...
[2015-09-04 08:43:44 UTC]  Poison Ivy Version: 2.32
[2015-09-04 08:43:44 UTC]  *** Host Information ***
PI profile ID: ctf
IP address: 192.168.0.100
Hostname: ADMIN-PC
Windows User: Administrator
Windows Version: Windows XP
Windows Build: 2600
Service Pack: Service Pack 3
[2015-09-04 08:43:58 UTC]  *** Directory Listing Initiated ***
Directory: C:\WINDOWS\
[2015-09-04 08:43:58 UTC]  *** Directory Listing Sent ***
[2015-09-04 08:44:57 UTC]  *** Service Listing Sent ***
[2015-09-04 08:45:06 UTC]  *** Screen Capture Sent ***
Shutting Down Modules ...
  Shutting Down poisonivy_23x
Module Shutdown Complete ...
ChopShop Complete
```

Nice. Now to save everything to disk:
```
$ ./chopshop 'poisonivy_23x -f -c -l' -f ../net.pcap
Warning Legacy Module poisonivy_23x!
Starting ChopShop
Initializing Modules ...
  Initializing module 'poisonivy_23x'
Running Modules ...
[2015-09-04 08:43:44 UTC]  Poison Ivy Version: 2.32
[2015-09-04 08:43:44 UTC]  *** Host Information ***
PI profile ID: ctf
IP address: 192.168.0.100
Hostname: ADMIN-PC
Windows User: Administrator
Windows Version: Windows XP
Windows Build: 2600
Service Pack: Service Pack 3
[2015-09-04 08:43:58 UTC]  *** Directory Listing Initiated ***
Directory: C:\WINDOWS\
[2015-09-04 08:43:58 UTC]  *** Directory Listing Sent ***
PI-directory-listing-1.txt saved..
[2015-09-04 08:44:57 UTC]  *** Service Listing Sent ***
PI-service-listing-2.txt saved..
[2015-09-04 08:45:06 UTC]  *** Screen Capture Sent ***
PI-extracted-file-3-screenshot.bmp saved..
Shutting Down Modules ...
  Shutting Down poisonivy_23x
Module Shutdown Complete ...
ChopShop Complete
```

Let's take a look at the files now: nothing too exciting in directory and service lisings, but once we open the screen capture, we hit the jackpot:

![](./screenshot.bmp?raw=true)

The flag is `TMCTF{May_Flower}`.
