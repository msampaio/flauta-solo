#UNIVERSIDADE FEDERAL DA BAHIA
#DEPARTAMENTO DE CIENCIA DA COMPUTACAO e ESCOLA DE MUSICA - GENOS
#PROJETO FINAL DE CURSO I - Orientadores: Marco Sampaio e Flavio Assis
# Danilo Azevedo Santos

import sys
def convertInt(cseq): # precisei disso pois necessitei marcar os CPs, e transformar numa saida legivel
	for i in range(len(cseq)-1):
		if type(cseq[i])!= int:
			cseq[i] = cseq[i].replace("+","").replace("-","")
			cseq[i] = int(cseq[i])

def tInput(entrada): # precisei disso para converter de string para int
    seq = []
    for i in range(len(entrada)):
        seq.append(int(entrada[i]))
    return seq

def maxima(seq, i, op): #devolve segmentos/lista de maxima
    if op == 0:
        return (seq[i+1] >= seq[i]) and (seq[i+1] >= seq[i+2])
    else:
        return (int(seq[i+1][0]) >= int(seq[i][0])) and (int(seq[i+1][0]) >= int(seq[i+2][0]))

def minima(seq, i, op): #devolve segmentos / lista de minimas
    if op == 0:
        return (seq[i+1] <= seq[i]) and (seq[i+1] <= seq[i+2])
    else:
        return (int(seq[i+1][0]) <= int(seq[i][0])) and (int(seq[i+1][0]) <= int(seq[i+2][0]))

def decision(cseq, a, b, op): # funcao de decisao para contorno mais proximos ou nao do primeiro e ultimo CP
    if op == 1:
        if a - 0 > len(cseq)-1 - b:
            return b
        elif a - 0 < len(cseq)-1 - b:
            return a
        else:
            return a
    else:
        if a - 0 > len(cseq)-1 - b:
            return a
        elif a - 0 < len(cseq)-1 - b:
            return b
        else:
            return b ## rever isso

def vCombination(cseq): # verificar se sinalizados sao combinacao de CPs adjacentes no contorno
    newList, i, logic = [], 0, None
    newList = vFlags(cseq)
    while (i < (len(newList)-1)):
        m,n = newList[i][1], newList[i+1][1]
        if n-m == 1 :
            if i+3 < len(newList):
                if newList[i][0] == newList[i+2][0] and newList[i+1][0] == newList[i+3][0]:
                    m, n= decision(cseq, m,m+2,0), decision(cseq, m+1,m+3,0)
                    cseq[m] = cseq[m].replace("+","").replace("-","")
                    cseq[m] = int(cseq[m])
                    cseq[n] = cseq[n].replace("+","").replace("-","")
                    cseq[n] = int(cseq[n])
                    logic = True
        if logic == True:
            i+=2
        else:
            i+=1
    return logic

def vFlags(cseq): # recolhe os sinalizados para vCombination
    newList = []
    for i in range(len(cseq)-1):
        if i != 0 and i != len(cseq)-1:
            if type(cseq[i]) == str:
                newList.append([cseq[i], i])
    return newList

def vMaxMin(lMax, lMin, cseq, N):# verifica se os cps sinalizados sao so maximas ou so minimas ou os dois
    newList = []
    newList.append(cseq[0])
    for i in range(len(cseq)):
        if type(cseq[i]) == str:
            newList.append(cseq[i])
    newList.append(cseq[len(cseq)-1])
    m,n,i = 0, 0, 1
    while (i < (len(newList)-1)):
        if newList[i][1] == '+':
            m=1
        else:
            n=1
        i+=1
    if m != 0 and n == 0:
        return True # os sinalizados sao maximas somente
    elif m == 0 and n != 0:
        return False # os sinalizados sao minimas somente
    else:
        return None # existe sinalizados maximas e minimas

def noFlags(cseq): # verificar se todos os CPs estao sinalizados
    m = 0
    for i in range(len(cseq)-1):
        if i != 0 and i != len(cseq)-1:
            if type(cseq[i]) == str:
                m +=1
    if m == len(cseq)-2:
        return True
    else:
        return False    			