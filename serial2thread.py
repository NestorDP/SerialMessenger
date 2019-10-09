#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:30:02 2018

@author: nestor
"""

import serial
import getopt
import sys
import _thread
#import time



############################################################################
#Função par receber dados
############################################################################
def get_data():
    while 1:
        byte_in = ser.read()
        msgIn = byte_in.decode()
        while byte_in.decode() != '\n':
            byte_in = ser.read()
            if byte_in.decode() == '\n':
                break
            msgIn = msgIn + byte_in.decode()
        mensagens.insert(0, msgIn) 
        print('')
############################################################################
#Função par enviar
############################################################################
def put_data():
    global flagEND
    while 1:
        msgOut = input()
        if msgOut != '#':
            ser.write(msgOut.encode())          # write a string
            ser.write(b'\n')    
            mensagens.insert(0, msgOut) 
        else:
            flagEND = 0



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

print ("============================================")
print ("Mensagem pra ser enviada:")
print ("============================================")

#
# Cria a thread
#===========================================================================
try:
   _thread.start_new_thread(get_data, () )
   _thread.start_new_thread(put_data, () )
except:
   print ("Error: unable to start thread")
   sys.exit(4)


#
# Laço que envia os dados 
#===========================================================================
mensagens = []
msgOut = 0
tamanho = 0
flagEND = 1
while flagEND:
   
    if tamanho < len(mensagens):
        sys.stdout.write('\u001b[0J')
        sys.stdout.flush()
        
        if len(mensagens) < 10:
            for x in range(0, len(mensagens)):                      # imprime a lista dos valores digitados
                print(mensagens[x])
            tamanho = len(mensagens)
            sys.stdout.write('\u001b['+str(len(mensagens)+1)+'F')   # Retorna o cursos para posição inicial
            sys.stdout.write('\u001b[0K')
            sys.stdout.flush()
        else:
            for x in range(0, 10):                                  # imprime a lista dos valores digitados
                print(mensagens[x])
            tamanho = len(mensagens)
            sys.stdout.write('\u001b[11F')                          # Retorna o cursos para posição inicial
            sys.stdout.write('\u001b[0K')
            sys.stdout.flush()

sys.stdout.write('\u001b[11E')  
print(mensagens)
