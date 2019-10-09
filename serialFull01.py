#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:58:07 2018

@author: nestor
"""
import serial
import getopt
import sys
import _thread

row = 1

#Função par receber dados
############################################################################
def get_data():
   global row
   while 1:
       byte_in = ser.read()
       msgIn = byte_in.decode()
       while byte_in.decode() != '\n':
           byte_in = ser.read()
           msgIn = msgIn + byte_in.decode()
       row = row + 1

       sys.stdout.write('\u001b['+str(row)+'EHe: '+msgIn+'\u001b['+str(7)+'H>>')
      
       
#
# Leitura e teste dos argumento de chamada do script
#===========================================================================
try:
    optlist, args = getopt.getopt(sys.argv[1:], 'P:b:')    
except getopt.GetoptError as err:
    print("ERROR:", err)  
    sys.exit(2)

#   
#Valores padrões dos argumentos do programa  
#===========================================================================
baud = 9600
porta = 0

#
#Arruma os argumentos nas respectivas variáveis
#===========================================================================
for opt, arg in optlist:
    if opt == '-P':
        porta = arg
    elif opt == '-b':
        baud = arg
if porta == 0:
    print('não foi selecionada uma porta')  
    sys.exit(3)      
        
print('Porta:', porta, '\nBaud Rate:', baud)

#
# Abre a comunicação com a porta serial escolhida
#===========================================================================
try:
    ser = serial.Serial(port=porta, baudrate=baud)  # open serial port
except serial.SerialException as err:    
    print("ERROR:", err)  
    sys.exit(3)
#
# Cria a thread
#===========================================================================
try:
   _thread.start_new_thread(get_data, () )
except:
   print ("Error: unable to start thread")
   sys.exit(4)

print ("============================================")
print ("Mensagem pra ser enviada:")
print ("============================================")

#
# Laço que envia os dados 
#===========================================================================
while 1:
    sys.stdout.write('\u001b[2K') #apaga a linha
    msgOut = input('>> ')
    sys.stdout.write('\u001b['+str(row)+'EI: '+msgOut+'\n') #cursor next line
    sys.stdout.write('\u001b['+str(row+2)+'F')              # volta o cursor

    
    row = row +1
    if msgOut != '#':
        ser.write(msgOut.encode())         # write a string
        ser.write(b'\n')
    else:
        break
    
sys.stdout.write('\u001b['+str(row+1)+'E') #cursor next line
ser.close()