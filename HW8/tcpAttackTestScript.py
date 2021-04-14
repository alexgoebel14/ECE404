# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:21:03 2021

@author: Alex
"""

from TcpAttack import *

spoofIP = '192.168.4.124'
targetIP = '127.0.0.1'
rangeStart = 9650
rangeEnd = 9750
port = 9700
Tcp = TcpAttack(spoofIP, targetIP)
Tcp.scanTarget(rangeStart, rangeEnd)
if Tcp.attackTarget(port,10):
    print('port was open for attack')