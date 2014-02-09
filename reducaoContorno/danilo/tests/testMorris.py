#!/usr/bin/env python
# -*- coding: utf-8 -*
#DEPARTAMENTO DE CIENCIA DA COMPUTACAO e ESCOLA DE MUSICA - GENOS - UFBA
#PROJETO FINAL DE CURSO I - Orientadores: Marco Sampaio e Flavio Assis
# Danilo Azevedo Santos


import unittest
import Morris.reductionMorris as morris


class MorrisTest():
	
	
	def testStep1():
		contour = [2, 3, 6, 4, 2, 1]
		assert morris.etapa1(contour,0) == [2, 6, 1]


	def testStep2():
		contour = [2, 5, 3, 4, 2, 1]
		assert morris.etapa2(contour,0) == [2, 3, 1]

	
	def testStep31():
		mx = [2,5,4,1]
    	mn = [2,3,1]
    	contour = [2, 5, 3, 4, 1]
    	assert morris.etapa3(contour,mx,mn,0) == [2, 5, 3, 4, 1]

    
	def testStep6():
		mx = [2, 4, 4, 5, 1]
     	contour = [2, 4, 4, 3, 5, 2, 1]
     	assert morris.etapa6(mx, contour) == [2, 4, 5, 1]

    
	def testStep7():
		mn = [2, 3, 4, 4, 1]
     	contour = [2, 6, 3, 5, 4, 5, 4, 7, 1]
     	assert morris.etapa7(mn, contour) == [2, 3, 4, 1]

    
	def testStep9():
		contour = [1,2,3,4]
    	assert morris.etapa9(contour, 0) == [1,2,3,4] 

main = MorrisTest()
main.testStep1()
main.testStep2()
main.testStep31()
main.testStep6()
main.testStep7()
main.testStep9()    		 	