#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 17:05:35 2018

@author: nestor
"""

import serial
import getopt
import sys
import _thread
#import time




#Função par receber dados
############################################################################
def get_data():
    global mensagens
    while 1:
        byte_in = ser.read()
        msgIn = byte_in.decode()
        while byte_in.decode() != '\n':
           byte_in = ser.read()
           msgIn = msgIn + byte_in.decode()
            
        mensagens.insert(0, msgIn) 

        #testa o tamanho da lista de valores lidos
        #===================================================================================
        if len(mensagens) < 10:                 # faz se a quantidade de elementos for menor que 10
            mensagens.insert(0, msgIn)         # insere o ultimo valor lido na posição 0 da lista           
            sys.stdout.write('\u001b[0J')       # apaga a tela 
            sys.stdout.flush()
            for x in range(0, len(mensagens)):  # imprime a lista dos valores digitados
                print(mensagens[x])
            sys.stdout.write('\u001b['+str(len(mensagens)-1)+'F')   # Retorna o cursos para posição inicial
            sys.stdout.flush()
        else:                                   # se for maior que 10
            mensagens.insert(0, msgIn)
            sys.stdout.write('\u001b[0J')       # apaga a tela
            sys.stdout.flush()
            for x in range(0, 10):              # iprime apenas as 10 primeiras posições
                print(mensagens[x])
            sys.stdout.write('\u001b['+str(9)+'F')
            sys.stdout.flush()
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
mensagens = []
msgOut = 0

while msgOut != '#':
    sys.stdout.write('\u001b[2K')           #apaga a linha
    msgOut = input('>> ')
    
    if msgOut != '#':
        ser.write(msgOut.encode())          # write a string
        ser.write(b'\n')

   
    #testa o tamanho da lista de valores lidos
    #===================================================================================
    if len(mensagens) < 10:                 # faz se a quantidade de elementos for menor que 10
        mensagens.insert(0, msgOut)         # insere o ultimo valor lido na posição 0 da lista           
        sys.stdout.write('\u001b[0J')       # apaga a tela 
        for x in range(0, len(mensagens)):  # imprime a lista dos valores digitados
            print(mensagens[x])
        sys.stdout.write('\u001b['+str(len(mensagens)+1)+'F')   # Retorna o cursos para posição inicial
    else:                                   # se for maior que 10
        mensagens.insert(0, msgOut)
        sys.stdout.write('\u001b[0J')       # apaga a tela
        for x in range(0, 10):              # iprime apenas as 10 primeiras posições
            print(mensagens[x])
        sys.stdout.write('\u001b['+str(11)+'F') 
    


ser.close()





"""
var = '0'
while var != '#end':
    sys.stdout.write('\u001b[2K')       #apaga a linha
    var = input('>> ')                  # Ler um valor do teclado
    
    #testa o tamanho da lista de valores lidos
    #===================================================================================
    if len(mensagens) < 10:                 # faz se a quantidade de elementos for menor que 10
        mensagens.insert(0, var)            # insere o ultimo valor lido na posição 0 da lista           
        sys.stdout.write('\u001b[0J')       # apaga a tela 
        for x in range(0, len(mensagens)):  # imprime a lista dos valores digitados
            print(mensagens[x])
        sys.stdout.write('\u001b['+str(len(mensagens)+1)+'F')   # Retorna o cursos para posição inicial
    else:                                   # se for maior que 10
        mensagens.insert(0, var)
        sys.stdout.write('\u001b[0J')       # apaga a tela
        
        for x in range(0, 10):              # iprime apenas as 10 primeiras posições
            print(mensagens[x])
        sys.stdout.write('\u001b['+str(11)+'F') 
    
print('\n')
sys.stdout.write('\u001b[10EFIM!\n')
print(mensagens)"""
