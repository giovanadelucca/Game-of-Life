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
     
    def set_media(self):
        self.media = self.dataframe.mean()
    
    def set_variancia(self):
        self.variancia = self.dataframe.var()  

    def set_desvio(self):
        self.desvio = self.dataframe.std()

    def set_soma(self):
        self.soma = self.dataframe.sum()

    def grafico1(self, name):
        sns.barplot(x=self.media[0],y=self.media[1],data=self.media)
        sns.savefig('data/files/graficos/'+ name + '.pdf')

    def grafico2(self, name):
        sns.barplot(x=self.variancia[0],y=self.variancia[1],data=self.variancia)
        sns.savefig('data/files/graficos/'+ name + '.pdf')

    def grafico3(self, name):
        sns.barplot(x=self.desvio[0],y=self.desvio[1],data=self.desvio)
        sns.savefig('data/files/graficos/'+ name + '.pdf')

    def grafico4(self, name):
        sns.barplot(x=self.soma[0],y=self.desvio[1],data=self.soma)
        sns.savefig('data/files/graficos/'+ name + '.pdf')

    def get_data_frame(self, path):
        return pd.read_csv(path, encoding = 'utf8') 

    def __init__(self, name):
        path = 'data/files/csv/' + name
        self.dataframe = self.get_data_frame(path)
        print(self.dataframe)
        self.media=pd.DataFrame() 
        self.variancia=pd.DataFrame()
        self.desvio=pd.DataFrame()
        self.soma=pd.DataFrame()
    
    def set_graficos(self, name):
        self.set_media()
        self.set_variancia()
        self.set_desvio()
        self.set_soma()
        self.grafico1(name)
        self.grafico2(name)
        self.grafico3(name)
        self.grafico4(name)
        
if __name__ == '__main__':
    est_r_pentomino = Estatistica('r-pentomino.csv')
    est_r_pentomino.set_graficos('r-pentomino')
    est_space_invaders = Estatistica('space_invaders.csv')
    est_space_invaders.set_graficos('space_invaders')
    est_space_invaders1 = Estatistica('space_invaders1.csv')
    est_space_invaders1.set_graficos('space_invaders1')
    est_start_random = Estatistica('start_random.csv')
    est_start_random.set_graficos('start_random')