#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 09:09:20 2018

@author: nestor
"""

import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
while 1:
    mensagem = input()
    if mensagem[0] == '#':
        break
    else:
        ser.write(mensagem.encode())         # write a string
        ser.write(b'\n')


ser.close()