#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 2, 2016

@author: Nicoli,Emanuel
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
        #print('media',self.media)
        
    def set_variancia(self):
        self.variancia = self.dataframe.var()
        print('variancia',self.variancia)
        

    def set_desvio(self):
        self.desvio = self.dataframe.std()
        #print('desvio',self.desvio)
        
    def set_soma(self):
        self.soma = self.dataframe.sum()
        #print('soma',self.soma)

    def set_lista(self):
        self.padroes.append('BGE')
        self.padroes.append('BON')
        self.padroes.append('BVE')
        self.padroes.append('BER')
        self.padroes.append('BCK')
        self.padroes.append('BAT')
        self.padroes.append('GER')
        self.padroes.append('HRY')
        self.padroes.append('HET')
        self.padroes.append('LAF')
        self.padroes.append('LGE')
        self.padroes.append('LAT')
        self.padroes.append('MGO')
        self.padroes.append('PND')
        self.padroes.append('SIP')
        self.padroes.append('TAD')
        self.padroes.append('TUB')
        #print(type(self.padroes))


    def grafico1(self, name):
        sns.barplot(x=self.padroes,y=self.media.values,palette='Greys')
        sns.plt.xlabel('Padroes')
        sns.plt.ylabel('Media')
        sns.plt.savefig('data/files/graficos/'+ name + 'media' + '.pdf')

    def grafico2(self, name):
        sns.barplot(x=self.padroes,y=self.variancia.values,palette='Greys')
        sns.plt.xlabel('Padroes')
        sns.plt.ylabel('Variancia')
        sns.plt.savefig('data/files/graficos/'+ name + 'variancia' + '.pdf')

    def grafico3(self, name):
        sns.barplot(x=self.padroes,y=self.desvio.values,palette='Greys')
        sns.plt.xlabel('Padrao')
        sns.plt.ylabel('Desvio')
        sns.plt.savefig('data/files/graficos/'+ name + 'desvio' + '.pdf')

    def grafico4(self, name):
        sns.barplot(x=self.padroes,y=self.soma.values,palette='Greys')
        sns.plt.xlabel('Padroes')
        sns.plt.ylabel('Quantidade')
        sns.plt.savefig('data/files/graficos/'+ name + 'bla' + '.pdf')

    def get_data_frame(self, path):
        return pd.read_csv(path, encoding = 'utf8') 

    def __init__(self, name):
        path = 'data/files/csv/' + name
        self.dataframe = self.get_data_frame(path)
        #print(self.dataframe)
        self.media=pd.DataFrame()
        self.variancia=pd.DataFrame()
        self.desvio=pd.DataFrame()
        self.soma=pd.DataFrame()
        self.padroes=[]
    
    def set_graficos(self, name):
        self.set_media()
        self.set_variancia()
        self.set_desvio()
        self.set_soma()
        self.set_lista()
        #self.grafico1(name)
        #self.grafico2(name)
        #self.grafico3(name)
        #self.grafico4(name)
        
if __name__ == '__main__':
    '''est_r_pentomino = Estatistica('r-pentomino.csv')
    est_r_pentomino.set_graficos('r-pentomino')
    est_space_invaders = Estatistica('space_invaders.csv')
    est_space_invaders.set_graficos('space_invaders')
    est_space_invaders1 = Estatistica('space_invaders1.csv')
    est_space_invaders1.set_graficos('space_invaders1')
    '''
    est_start_random = Estatistica('start_random.csv')
    est_start_random.set_graficos('start_random')
