#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 09:09:20 2018

@author: nestor
"""

from serial.tools.list_ports import comports

p = comports()
lenPorts = len(p)
available = [port[0] for port in p] #list comprehension

for x in range(0, lenPorts):
    print(p[x])
    
    
