
import aux

class Contour:
	
	 def __init__(self, cseq):
	 	self.cseq = cseq
	 	#self.reductBor(3, self.cseq)

	 def reductBor(self):
	 	k, newList =0, []
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
    entrada = raw_input("(entrada - ex: 1 2 3 4): ")
    entrada = entrada.split(" ")
    contour = aux.convert_input(entrada)
    obj = Contour(contour)
    print " (", obj.reductBor(), " 3 )" 
      
# # # Main program, a place that we call the functions above # # #
main()  #Final process    	 	