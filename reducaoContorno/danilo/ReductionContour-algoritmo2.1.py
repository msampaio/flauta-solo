def maxima(seq, i):
    return (seq[i+1] >= seq[i]) and (seq[i+1] >= seq[i+2])

def minima(seq, i):
    return (seq[i+1] <= seq[i]) and (seq[i+1] <= seq[i+2])

def Etapa1 (contour,N):
    i = 0
    listaMaxima = []
    if (N == 0):
        listaMaxima.append(contour[0])
        while (i < (len(contour)-2)):
            if(i <= len(contour) and maxima(contour,i)):
                listaMaxima.append(contour[i+1])
            i+=1
    listaMaxima.append(contour[len(contour)-1])
    return listaMaxima

def Etapa2 (contour,N):
    i = 0
    listaMinima = []
    if (N == 0):
        listaMinima.append(contour[0])
        while (i < (len(contour)-2)):
            if(i <= len(contour) and minima(contour,i)):
                listaMinima.append(contour[i+1])
            i+=1
    listaMinima.append(contour[len(contour)-1])
    return listaMinima

def Etapa3 (contour, lMax, lMin, N):
    a = set(lMax).union(set(lMin))
    b = set(contour)
    c = b.difference(a)
    flag = list(a)
    noflag = PegaNoSinalizado(list(c), contour)
    print "etapa 3 -> lista de sinalizados:" ,flag, "lista de nao sinalizados:",noflag
    if (c == set([])):
        N+=1
        return Etapa9(contour,N)
    else:
        return Etapa4 (noflag,contour,N,lMax,lMin)

def Etapa4 (noflag, contour, N,lmx, lmn):
    #for i in range(len(noflag)):
    j = 0
    for i in range(len(contour)-1):
        if j < len(noflag):
            if (int(noflag[j]) == int(contour[i])):
                del contour[i]
                j+=1
    return Etapa5(contour, N,lmx,lmn)

def Etapa5 (contour, N,lmx,lmn):
    N+=1
    print "etapas 4 e 5 -> Novo Contorno",contour
    print "nivel de profundidade: N = %d" %N
    return Etapa8(contour,lmx,lmn,N)

def Etapa6 (lMax,contour):
    i = 0
    k = 0
    newList = []
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
    i = 0
    k = 0
    newList = []
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
    nlMax = []
    nlMin = []
    nlMax = Etapa6(lMax,contour)
    nlMin = Etapa7(lMin,contour)
    print "etapas 6, 7 e 8 -> listademaximo: ",nlMax," listademinimo: ",nlMin
    return Etapa3(contour,nlMax,nlMin,N)

def Etapa9 (contour,N):
    print "etapa 9 melodia reduzida: Contorno Final", contour
    print "nivel de profundidade: N = %d" %N

def TransfInput(entrada):
    seq = []
    for i in range(len(entrada)):
        seq.append(int(entrada[i]))
    return seq

def PegaNoSinalizado(input1, input2):
    saida = []
    for i in range(len(input1)):
        for j in range(len(input2)):
            if input2[j] == input1[i]:
                saida.append(input1[i])
    return saida


### programa principal onde chamamos as funcoes acima ###
entrada = raw_input("entre com os contorno formato de entrada ex: 1 2 3 4 (separados por um espaco): ")
str1 = entrada.split(" ")
contour=[]
contour = TransfInput(str1)
print "Contorno Original: ",contour
i = 0
# Etapa0(n)
n = 0
lmax = []
lmin = []
lmax = Etapa1(contour,n)
lmin = Etapa2(contour,n)
print "etapas 0, 1 e 2 -> N = %i" %n,"listademaximo:",lmax,"listademinimo:",lmin
Etapa3 (contour, lmax, lmin, n)



