#UNIVERSIDADE FEDERAL DA BAHIA
#DEPARTAMENTO DE CIENCIA DA COMPUTACAO e ESCOLA DE MUSICA - GENOS
#PROJETO FINAL DE CURSO I - Orientadores: Marco Sampaio e Flavio Assis
# Danilo Azevedo Santos


import aux


class Contour:
	""" class create object contour by functions of the
	algorithms"""

	
	 def __init__(self, cseq):
	 	"""initialize class contour, its receive object
	 	and set of input in object"""

	 	self.cseq = cseq
	 	#self.reductBor(3, self.cseq)


	 def reductBor(self):
	 	"""Returns a contour segment reduced by Bor Window Algorithm.
	 	exemple input Contour([0 3 2 1]) and return ([0 3 1], 3)"""

	 	k, newList = 0, []
	 	size = len(self.cseq)
	 	newList.append(self.cseq[0])
	 	for i in range(size -2):
	 		if i != size :
	 			if aux.maxima(self.cseq, i) or aux.minima(self.cseq, i):
	 				if self.cseq[i+1] != newList[k]:
	 					newList.append(self.cseq[i+1])
	 					k +=1
	 	newList.append(self.cseq[size -1])
	 	self.cseq = []
	 	self.cseq = newList[:]
	 	return self.cseq



def main():
	"""Returns the execution algorithms, the metod 
	can be removed and replaced by automatic testing future"""

    entrada = raw_input(" ")
    entrada = entrada.split(" ")
    contour = aux.convert_input(entrada)
    obj = Contour(contour)
    print " (", obj.reductBor(), " 3 )" 
      
"""Main program, a place that we call the functions above"""
main()  #Final process    	 	