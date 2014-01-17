#!/usr/bin/env python
# -*- coding: utf-8 -*
#DEPARTAMENTO DE CIENCIA DA COMPUTACAO e ESCOLA DE MUSICA - GENOS - UFBA
#PROJETO FINAL DE CURSO I - Orientadores: Marco Sampaio e Flavio Assis
# Danilo Azevedo Santos


def maxima(seq, i):
    """returns the max c-pitch contour of a suit"""


    return (seq[i+1] >= seq[i]) and (seq[i+1] >= seq[i+2])


def minima(seq, i):
    """"returns the max c-pitch contour of a suit"""


    return (seq[i+1] <= seq[i]) and (seq[i+1] <= seq[i+2])


def Etapa1 (contour,N):
    """Set the list of maximum of the contour
    """

    i,listaMaxima = 0, []
    if (N == 0):
        listaMaxima.append(contour[0])
        while (i < (len(contour)-2)):
            if(i <= len(contour) and maxima(contour,i)):
                listaMaxima.append(contour[i+1])
            i+=1
    listaMaxima.append(contour[len(contour)-1])
    return listaMaxima


def Etapa2 (contour,N):
    """Set the list of minimum of the contour
    """


    i, listaMinima = 0,[]
    if (N == 0):
        listaMinima.append(contour[0])
        while (i < (len(contour)-2)):
            if(i <= len(contour) and minima(contour,i)):
                listaMinima.append(contour[i+1])
            i+=1
    listaMinima.append(contour[len(contour)-1])
    return listaMinima


def Etapa3 (contour, lMax, lMin, N):
    """check which CP was not flagged in the maximum and minimum 
       The difference between C - listaMaximaUlistaminima {} = 0, 
       then jumps to step 9, if override: = C - {listaMaxima listaMinima U} = 0 then 
       Step 9 returns (C) but aid = C - {listaMaxima listaMinima U} = [difference CP] 
       return step 4 (auxiliary, C)
    """


    a,b = set(lMax).union(set(lMin)), set(contour)
    c = b.difference(a)
    flag, noflag = list(a), PegaNoSinalizado(list(c), contour)
    if (c == set([])):
        N+=1
        return Etapa9(contour,N)
    else:
        return Etapa4 (noflag,contour,N,lMax,lMin)


def Etapa4 (noflag, contour, N,lmx, lmn):
    """check which auxiliary station in C 
     C. remove.de.C if [ai] = helper [ak] 
     return step 5 (C, N)"""


    j = 0
    for i in range(len(contour)-1):
        if j < len(noflag):
            if (int(noflag[j]) == int(contour[i])):
                del contour[i]
                j+=1
    return Etapa5(contour, N,lmx,lmn)


def Etapa5 (contour, N,lmx,lmn):
    """Here the increase of the reduction profudidade 1 occurs, ie, N = N +1
    """
    N+=1
    return Etapa8(contour,lmx,lmn,N)


def Etapa6 (lMax,contour):
    """novalistaMaxima = MAX {} listaMaxima 
    loop if listaMaxima [al] = listaMaxima [ak] 
    removes novalistaMaxima [al] = listaMaxima [al] 
    return novalistaMaxima"""


    i, k, newList = 0, 0, []
    newList.append(lMax[0])
    while (i < (len(lMax)-2)):
        if (maxima(lMax,i)):
            if(lMax[i+1] != newList[k]):
                k+=1
                newList.append(lMax[i+1])
            elif ((lMax[i+1] == lMax[0]) or ((lMax[i+1] == lMax[len(lMax)-1]))):
                n = contour.index(lMax[i+1])
                contour.pop(n)
            else:
                n = contour.index(lMax[i+1])
                contour.pop(n)
        i+=1
    newList.append(lMax[len(lMax)-1])
    return newList


def Etapa7 (lMin,contour):
    """novalistaMinima = MAX {} listaMinima 
       loop if listaMinima [al] = listaMinima [ak] 
       removes novalistaMinima [al] = listaMinima [al] 
       return novalistaMinima"""


    i,k, newList = 0, 0, []
    newList.append(lMin[0])
    while (i < (len(lMin)-2)):
        if (minima(lMin,i)):
            if(lMin[i+1] != newList[k]):
                k+=1
                newList.append(lMin[i+1])
            elif ((lMin[i+1] == lMin[0]) or ((lMin[i+1] == lMin[len(lMin)-1]))):
                n = contour.index(lMin[i+1])
                contour.pop(n)
            else:
                n = contour.index(lMin[i+1])
                contour.pop(n)
        i+=1
    newList.append(lMin[len(lMin)-1])
    return newList


def Etapa8 (contour, lMax, lMin, N):
    """Here we have an interaction that back to step 3, 
    so that further checks occur on the new contour
    and also check if the outline is in prime form
    """


    nlMax, nlMin = [], []
    nlMax, nlMin = Etapa6(lMax,contour), Etapa7(lMin,contour)
    return Etapa3(contour,nlMax,nlMin,N)


def Etapa9 (contour,N):
    """the final stage has become the new boundary"""


    print "Contorno Final", contour
    print "Profundidade: N = %d" %N


def convertInput(entrada):
    """function to modify the input to run the algorithm 
    with code list as input is given in string"""


    seq = []
    for i in range(len(entrada)):
        seq.append(int(entrada[i]))
    return seq


def PegaNoSinalizado(input1, input2):
    """the quantity no flags contour"""


    saida = []
    for i in range(len(input1)):
        for j in range(len(input2)):
            if input2[j] == input1[i]:
                saida.append(input1[i])
    return saida


# # # Main program, a place that we call the functions above # # #

entrada = raw_input("(entrada - ex: 1 2 3 4): ")
str1 = entrada.split(" ")
contour=[]
contour = convertInput(str1)
print "Contorno Original: ",contour
i = 0

# Step 0 of the algorithm sets the depth value
n = 0
lmax, lmin = [],[]
lmax, lmin = Etapa1(contour,n), Etapa2(contour,n)
Etapa3 (contour, lmax, lmin, n)