#UNIVERSIDADE FEDERAL DA BAHIA
#DEPARTAMENTO DE CIENCIA DA COMPUTACAO e ESCOLA DE MUSICA - GENOS
#PROJETO FINAL DE CURSO I - Orientadores: Marco Sampaio e Flavio Assis
# Danilo Azevedo Santos

import sys
import Aux

# entao, a estrutura desse algoritmo para o de Morris foi diferente nos aspectos mais importantes,
# pois para determinada execucao do algoritmo apareceram algumas situacoes que pediram tais 
# tratamentos seque descricao abaixo

def Step1 (cseq): #uma das mundacas foi no tratamento de maximas e minimas
    i, listaMaxima = 0,[]# pois precisei guarda na listamax
    listaMaxima.append([cseq[0], 0])# e listamin o valor do CP e a sua posicao
    while (i < (len(cseq)-2)):
        if(i <= len(cseq) and Aux.maxima(cseq,i,0)):
            listaMaxima.append([cseq[i+1], i+1])
            cseq[i+1] = str(cseq[i+1])+'+'
        i+=1
    listaMaxima.append([cseq[len(cseq)-1], len(cseq)-1])
    return listaMaxima

def Step2 (cseq):
    i, listaMinima =0, []
    listaMinima.append([cseq[0],0])
    while (i < (len(cseq)-2)):
        if(i <= len(cseq) and Aux.minima(cseq,i,0)):
            listaMinima.append([cseq[i+1],i+1])
            cseq[i+1] = str(cseq[i+1])+'-'
        i+=1
    listaMinima.append([cseq[len(cseq)-1],len(cseq)-1])
    return listaMinima

def Step3 (cseq, Max, Min, N): # Etapa faz o teste de todos os CPs excetos o 1o e o ultimo
    k = Aux.noFlags(cseq)#pois ja sao sinalizados por definicao
    if k != True:
        return Step4a5(cseq, N, Max, Min)
    else:
        return Step6(cseq, Max, Min, N)

def Step4a5 (cseq, N, Max, Min):# preciso ver isso ainda ##em teste##
    for i in range(len(cseq)-1):
        if i < len(cseq):
            if (i != 0 and i != len(cseq)-1):
                    if type(cseq[i]) != str:
                        del cseq[i]
    N+=1
    print "Novo Contorno %d" %N," : ", cseq
    return Step6(cseq, Max,Min,N)

def Step6 (cseq, Max, Min, N):#etapas 6 e 7 que verificar se ha adjacentes repetidos, mas
    i, newList = 0, [] # nao exclui estes
    newList.append(Max[0])
    while (i < (len(Max)-2)):
        if (Aux.maxima(Max,i,1)):
            if ((Max[i+1][0] != Max[0][0]) and ((Max[i+1][0] != Max[len(Max)-1][0]))):
                newList.append(Max[i+1])
        else:
            n = Max[i+1][1]
            if type(cseq[n]) == str:
                cseq[n] = cseq[n].replace("+","")
                cseq[n] = int(cseq[n])
        i+=1
    newList.append(Max[len(Max)-1])
    Max = []
    Max = newList[:]
    return Step7(cseq, Max, Min, N)

def Step7 (cseq, Max, Min, N):
    i, newList = 0, []
    newList.append(Min[0])
    while (i < (len(Min)-2)):
        if (Aux.minima(Min,i,1)):
            if ((Min[i+1][0] != Min[0][0]) and ((Min[i+1][0] != Min[len(Min)-1][0]))):
                newList.append(Min[i+1])
        else:
            n = Min[i+1][1]
            if type(cseq[n]) == str:
                cseq[n] = cseq[n].replace("-","")
                cseq[n] = int(cseq[n])
        i+=1
    newList.append(Min[len(Min)-1])
    Min = []
    Min = newList[:]
    return Step8(cseq, Max, Min, N)

def Step8 (cseq, Max, Min, N):# verifica se ha uma minimas entre maximas adjacentes repetidas
    i = 1
    while (i < (len(Max)-2)):
        if Max[i][0] == Max[i+1][0]: # testa se sao iguais
            if Max[i+1][1] - Max[i][1] == 2: # testa se sao adjacentes
                a = Max[i][1]
                if type(cseq[a+1]) != int: # testa se nao e sinalizado
                    if cseq[a+1][1] != '-': # testa se tem minima entre eles
                        a = Aux.decision(cseq, a, a+2,1)
                        cseq[a] = cseq[a].replace("+","")
                        cseq[a] = int(cseq[a])
                else:
                    a = Aux.decision(cseq, a, a+2,1)
                    cseq[a] = cseq[a].replace("+","")
                    cseq[a] = int(cseq[a])
        i+=1
    return Step9(cseq, Max, Min, N)

def Step9 (cseq, Max, Min, N):# verifica se ha uma maximas entre minimas adjacentes repetidas
    i = 1
    while (i < (len(Min)-2)):
        if Min[i][0] == Min[i+1][0]: # testa se sao iguais
            if Min[i+1][1] - Min[i][1] == 2: # testa se sao adjacentes
                a = Min[i][1]
                if type(cseq[a+1]) != int: # testa se nao e sinalizado
                    if cseq[a+1][1] != '+': # testa se tem maxima entre eles
                        a = Aux.decision(cseq, a, a+2,1)
                        cseq[a] = cseq[a].replace("-","")
                        cseq[a] = int(cseq[a])
                else:
                    a = Aux.decision(cseq, a, a+2,1)
                    cseq[a] = cseq[a].replace("-","")
                    cseq[a] = int(cseq[a])
        i+=1
    return Step10a13(cseq, Max, Min, N)

def Step10a13(cseq, Max, Min, N):
    if Aux.noFlags(cseq) == True:# etapa 10.1 verificar se todos os cps estao sinalizados
        if (Aux.vCombination(cseq) != True):# se passa da 10.1 entra na etapa 10.2 verifica combinacao de cps
            return Step17(cseq, N) # se passar na 10.1 e 10.2 vai para final
    else:
        Aux.vCombination(cseq) # etapa 11 desmacar as combinacoes de cps
        logic =  Aux.vMaxMin(Max, Min, cseq, N) # etapa 12
        if logic == True: # add uma minima
            print ''
        elif logic == False:# add uma maxima
            print ''
        else: # deixa como esta
            print ''
    newList = []
    newList.append(cseq[0])
    for i in range(len(cseq)-1): # etapa 13
        if i != 0 and type(cseq[i]) == str:
            newList.append(cseq[i])
    newList.append(cseq[len(cseq)-1])
    cseq =[]
    cseq = newList[:]
    return Step14a16(cseq, Max, Min, N)

def Step14a16(cseq, Max, Min, N):
    if N != 0: # etapa 14
        N+=1
    else:   # etapa 15
        N+=2
    Aux.convertInt(cseq)
    Max,Min = Step1(cseq), Step2(cseq)
    return Step6(cseq, Max, Min, N)

def Step17 (cseq, N):
    Aux.convertInt(cseq)
    print "melodia reduzida: ",cseq,"\n -> N = %d" %N
    #return sys.exit()

if __name__ == "__main__":# desativei alguns prints, se quiser ative-os tera maior legibilidade do algoritmo
    entrada = raw_input("entrada ex:1 2 3 separados p/ espacos: ")# a
    str1, contour = entrada.split(" "), []
    contour = Aux.tInput(str1)
    C = contour[:]
    i,n,lmax,lmin = 0,0,[],[]
    lmax, lmin = Step1(contour), Step2(contour)
    #print "etapas iniciais-> N = %i" %n,"\nlistademax:",lmax,"\nlistademin:",lmin
    Step3 (contour, lmax, lmin, n)
    print "Contorno Original: ",C
