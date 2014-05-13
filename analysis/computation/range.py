import numpy
import json

def range_analysis(compositions):
    range_list = [c.music_data.ambitus for c in compositions]

    # ambitus frequency analysis - for histogram
    frequency = {}
    for v in range_list:
        if(v not in frequency):
            frequency[v] = 0
        frequency[v] +=1


    # teste para gerar gráfico.
    r = [
    {
        "key": "Cumulative Return",
        "values": [
            {
                "label" : "A" ,
                "value" : 29.765957771107
            } ,
            {
                "label" : "B" ,
                "value" : 0
            } ,
            {
                "label" : "C" ,
                "value" : 32.807804682612
            } ,
            {
                "label" : "D" ,
                "value" : 196.45946739256
            } ,
            {
                "label" : "E" ,
                "value" : 0.19434030906893
            } ,
            {
                "label" : "F" ,
                "value" : 98.079782601442
            } ,
            {
                "label" : "G" ,
                "value" : 13.925743130903
            } ,
            {
                "label" : "H" ,
                "value" : 5.1387322875705
            }
        ]
    }
    ]

    return json.dumps(r)
    # range_statistics = {}
    # range_statistics['Min'] = min(range_list)
    # range_statistics['Max'] = max(range_list)
    # range_statistics['Mean'] = numpy.mean(range_list)
    # range_statistics['Standard deviation'] = numpy.std(range_list)
    #
    # return range_statistics
