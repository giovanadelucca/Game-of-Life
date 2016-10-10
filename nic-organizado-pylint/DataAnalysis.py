'''
Created on Oct 2, 2016

@author: Nicoli
'''

import pandas as pd

import numpy as np

import seaborn as sns

    
class Estatistica(object):
    '''
    classdocs
    '''
     
    def media(self):
         
        self.media=self.dataframe.mean()
    
    
    def variancia(self):
    
        self.variancia=self.dataframe.var()  
       
       
    
    def desvio(self):
        self.desvio=self.dataframe.std()
    
    def soma(self):
        self.soma=self.dataframe.sum()
    
    def grafico1(self):
        sns.barplot(x=self.media[0],y=self.media[1],data=self.media)
        sns.savefig("poe o caminho aqui")
    
    def grafico2(self):
        sns.barplot(x=self.variancia[0],y=self.variancia[1],data=self.variancia)
        sns.savefig()
    
    def grafico3(self):
        sns.barplot(x=self.desvio[0],y=self.desvio[1],data=self.desvio)
        sns.savefig()
    
    def grafico4(self):
        sns.barplot(x=self.soma[0],y=self.desvio[1],data=self.soma)
        sns.savefig()
    
    
    
    def __init__(self):
        
        self.dataframe=self.get_data_frame(path)
               
        self.media={}        
        self.variancia={}
        self.desvio={}
    
        self.soma={}               
    
