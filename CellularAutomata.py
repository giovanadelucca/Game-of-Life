# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from IntKBase import IntKBase

class CellularAutomata(object):
    def __init__(self, neighborhood, rule):
        self.__neighborhood = neighborhood
        self.__rule = rule
        self.__k = 2

        self.__dictRule = self.setDictRule(self.neighborhood, self.rule, self.k)
        
    def setDictRule(self, neighborhood, rule, k):
        ruleInKBase = IntKBase(rule, k).numInBase
        numComb = self.k**neighborhood
        if (len(ruleInKBase) < numComb):
            while (len(ruleInKBase) < numComb):
                ruleInKBase = "0" + ruleInKBase 
        self.__dictRule = {}
        i = numComb-1
        for d in ruleInKBase:
            self.__dictRule[i] = int(d)
            i -=1
        return self.__dictRule
        
    def getState(self, chave):
        return self.dictRule[chave]
    
    @property
    def neighborhood(self):
        return self.__neighborhood
    
    @property
    def rule(self):
        return self.__rule
    
    @property
    def k(self):
        
        """
        Retorna k.
        """
        
        return self.__k
    
    @property
    def dictRule(self):
        return self.__dictRule
    
    @property
    def catype(self):
        return self.__catype
    
    @catype.setter
    def catype(self, catype):
        self.__catype = catype
        
    @property
    def seed(self):
        return self.__seed    
