# -*- coding: utf-8 -*-

from CellularAutomata import CellularAutomata

class BiOuterTotalisticCode(CellularAutomata):

    def __init__(self, neighborhood, rule):
        super(BiOuterTotalisticCode,self).__init__(neighborhood, rule)
        self.catype = 'OuterTotalistic'
        self.dimension = 'Bidimensional'
          
    def getNextNine (self, b1, b2, b3, b4, b5, b6, b7, b8, b9):
        temp = int(b1 + ((b2 + b3 + b4 + b5 + b6 + b7 + b8 + b9)*2))
        return self.dictRule[temp]
    
    def getNextFive (self, b1, b2, b3, b4, b5):
        temp = int(b1 + ((b2 + b3 + b4 + b5)*2))
        return self.dictRule[temp]
