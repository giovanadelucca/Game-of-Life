# -*- coding: utf-8 -*-

from CellularAutomata import CellularAutomata

class BiOuterTotalisticCode(CellularAutomata):

    def __init__(self, neighborhood, rule):
        """
        Construtor da subclasse BidimensionalCode
        Estende o método construtor de CellularAutomata.
        Também é instanciado o tipo do autômato: Bidimensional
        """
        super(BiOuterTotalisticCode,self).__init__(neighborhood, rule, k = 2, seed = 1)
        self.catype = 'OuterTotalistic'
        self.dimension = 'Bidimensional'
          
    def getNextNine (self, b1, b2, b3, b4, b5, b6, b7, b8, b9):
        
        temp = int(b1 + ((b2 + b3 + b4 + b5 + b6 + b7 + b8 + b9)*2))
        
        return self.dictRule[temp]
    
    def getNextFive (self, b1, b2, b3, b4, b5):
        
        temp = int(b1 + ((b2 + b3 + b4 + b5)*2))
        
        return self.dictRule[temp]