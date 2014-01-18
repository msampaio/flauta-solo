#!/usr/bin/env python
# -*- coding: utf-8 -*
#DEPARTAMENTO DE CIENCIA DA COMPUTACAO e ESCOLA DE MUSICA - GENOS - UFBA
#PROJETO FINAL DE CURSO I - Orientadores: Marco Sampaio e Flavio Assis
# Danilo Azevedo Santos


def catch_noflags(input1, input2):
    """the quantity no flags contour"""

    saida = []
    for i in range(len(input1)):
        for j in range(len(input2)):
            if input2[j] == input1[i]:
                saida.append(input1[i])
    return saida


def convert_input(entrada):
    """function to modify the input to run the algorithm
    with code list as input is given in string"""

    seq = []
    for i in range(len(entrada)):
        seq.append(int(entrada[i]))
    return seq

def maxima(seq, i):
    """returns the max c-pitch contour of a suit"""

    return (seq[i+1] >= seq[i])and(seq[i+1] >= seq[i+2])


def minima(seq, i):
    """"returns the max c-pitch contour of a suit"""

    return (seq[i+1] <= seq[i])and(seq[i+1] <= seq[i+2])  