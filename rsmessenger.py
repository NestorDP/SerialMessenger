#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 07:23:57 2018

@author: nestor
"""

import serial
import getopt
import sys
import _thread
#import time



############################################################################
#Função par receber dados (Thread)
############################################################################
def get_data():
    global flagTHREAD_GET
    while flagTHREAD_GET:
        byte_in = ser.read()
        msgIn = byte_in.decode()
        while byte_in.decode() != '\n':
            byte_in = ser.read()
            if byte_in.decode() == '\n':
                break
            msgIn = msgIn + byte_in.decode()
        mensagens.insert(0, 'Recebido: '+msgIn) 
        print('')
############################################################################
#Função par enviar (Thread)
############################################################################
def put_data():
    global flagEND
    global flagSAVE
    global flagTHREAD_PUT
    while flagTHREAD_PUT:
        msgOut = input()
        if msgOut == '#e':
            flagEND = 0
            flagTHREAD_PUT = 0
            flagTHREAD_GET = 0
        elif msgOut == '#s':
            flagEND = 0
            flagSAVE = 1
            flagTHREAD_PUT = 0
            flagTHREAD_GET = 0
        else:         
            ser.write((msgOut+'\n').encode())          # write a string
            #ser.write(b'\n')    
            mensagens.insert(0, 'Enviado:  '+msgOut) 
############################################################################
            
            
            
            
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

print ("\nMensagem pra ser enviada:")
print ("============================================\n")
print ("============================================")
sys.stdout.write('\u001b[2F')
sys.stdout.flush()

flagTHREAD_PUT = 1
flagTHREAD_GET = 1
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
flagSAVE = 0
while flagEND:
    if tamanho < len(mensagens):
        print ("============================================")
        sys.stdout.write('\u001b[0J')
        sys.stdout.flush()        

        sys.stdout.flush()
        if len(mensagens) < 10:
            for x in range(0, len(mensagens)):                      # imprime a lista dos valores digitados
                print(mensagens[x])
            tamanho = len(mensagens)
            sys.stdout.write('\u001b['+str(len(mensagens)+2)+'F')   # Retorna o cursos para posição inicial
            sys.stdout.write('\u001b[0K')
            sys.stdout.flush()
        else:
            for x in range(0, 10):                                  # imprime a lista dos valores digitados
                print(mensagens[x])
            tamanho = len(mensagens)
            sys.stdout.write('\u001b[12F')                          # Retorna o cursos para posição inicial
            sys.stdout.write('\u001b[0K')
            sys.stdout.flush()

sys.stdout.write('\u001b[12E')  
sys.stdout.flush()
print()
#for y in range(0, len(mensagens)):
#        print(mensagens[len(mensagens)-1 - y])

if flagSAVE:
    nome_arq = input('Nome do arquivo: ')
    arq = open(nome_arq+'.txt', 'w')
    for y in range(len(mensagens)-1, -1, -1):
        arq.write(mensagens[y]+'\n')
    arq.close()
    
#print(mensagens)