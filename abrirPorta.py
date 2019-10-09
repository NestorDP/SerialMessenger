#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 14:44:44 2018

@author: nestor
"""
import serial
ser = serial.Serial('/dev/pts/20')  # open serial port
while 1:
    mensagem = input()
    if mensagem[0] == '#':
        break
    else:
        ser.write(mensagem.encode())         # write a string
        ser.write(b'\n')


ser.close()