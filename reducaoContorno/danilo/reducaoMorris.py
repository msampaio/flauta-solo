# -*- coding: utf-8 -*-

def Etapa1  (C,N):
    i = 0
    listaMaxima = []
    if (N == 0):
        listaMaxima.append(C[0])
        while (i < (len(C)-2)):
            if((C[i+1] >= C[i]) and (C[i+1] >= C[i+2])):
                if(i <= len(C)):
                    listaMaxima.append(C[i+1])
            i+=1
    listaMaxima.append(C[len(C)-1])
    return listaMaxima

def Etapa2 (C,N):
    i = 0
    listaMinima = []
    if (N == 0):
        listaMinima.append(C[0])
        while (i < (len(C)-2)):
            if((C[i+1] <= C[i]) and (C[i+1] <= C[i+2])):
                if(i <= len(C)):
                    listaMinima.append(C[i+1])
            i+=1
    listaMinima.append(C[len(C)-1])
    return listaMinima

def Etapa3 (C, lMax, lMin,N):
    a = set(lMax).union(set(lMin))
    b = set(C)
    c = b.difference(a)
    Sinalizado = list(a)
    nSinalizado = list(c)
    print "etapa 3 -> lista de sinalizados:" ,Sinalizado, "lista de nao sinalizados:",nSinalizado
    if (c == set([])):
        N+=1
        return Etapa9(C,N)
    else:
        return Etapa4 (nSinalizado,C,N,lMax,lMin)

def Etapa4 (naoSinalizados, C, N,lmx, lmn):
    for i in range(len(naoSinalizados)):
        for j in range(len(C)-1):
            if (int(naoSinalizados[i]) == int(C[j])):
                C.pop(j)
    return Etapa5(C, N,lmx,lmn)

def Etapa5 (C, N,lmx,lmn):
    N+=1
    print"etapas 4 e 5 -> Novo Contorno",C
    print "nivel de profundidade: N = %d" %N
    return Etapa8(C,lmx,lmn,N)

def Etapa6 (lMax,C):
    i = 0
    k = 0
    newList = []
    newList.append(lMax[0])
    while (i < (len(lMax)-2)):
        if ((lMax[i+1] >= lMax[i]) and (lMax[i+1] >= lMax[i+2])):
            if(lMax[i+1] != newList[k]):
                k+=1
                newList.append(lMax[i+1])
            else:
                n = C.index(lMax[i+1])
                C.pop(n)
        i+=1
    newList.append(lMax[len(lMax)-1])
    return newList

def Etapa7 (lMin,C):
    i = 0
    k = 0
    newList = []
    newList.append(lMin[0])
    while (i < (len(lMin)-2)):
        if ((lMin[i+1] <= lMin[i]) and (lMin[i+1] <= lMin[i+2])):
            if(lMin[i+1] != newList[k]):
                k+=1
                newList.append(lMin[i+1])
            else:
                n = C.index(lMin[i+1])
                C.pop(n)
        i+=1
    newList.append(lMin[len(lMin)-1])
    return newList

def Etapa8 (C, lMax, lMin, N):
    nlMax = []
    nlMin = []
    nlMax = Etapa6(lMax,C)
    nlMin = Etapa7(lMin,C)
    print"etapas 6, 7 e 8 -> listademaximo: ",nlMax," listademinimo: ",nlMin
    return Etapa3(C,nlMax,nlMin,N)

def Etapa9 (C,N):
    print "etapa 9 melodia reduzida: Contorno Final", C
    print "nivel de profundidade: N = %d" %N

def TransfInput(entrada):
    C = []
    for i in range(len(entrada)):
        if ((str1[i] != ' ')):
            C.append(int(entrada[i]))
    return C

# FIXME: remover
# ### programa principal onde chamamos as funcoes acima ###
# str1 = raw_input("entre com os contorno formato de entrada ex: 1234 ou 1 2 3 4: ")
# C = TransfInput(str1)
# print"Contorno Original: ",C
# i = 0
# # Etapa0(n)
# n = 0
# lmax = []
# lmin = []
# Contorno = []
# lmax = Etapa1(C,n)
# lmin = Etapa2(C,n)
# print "etapas 0, 1 e 2 -> N = %i" %n,"listademaximo:",lmax,"listademinimo:",lmin
# Etapa3 (C, lmax, lmin, n)
