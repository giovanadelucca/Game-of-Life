#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Nicoli
'''

import numpy as np

class Patterns():
    '''doc
    '''
    def start_mat(self, from_pygame):
        '''doc
        '''
        mat = np.zeros([self.map_size, self.map_size])
        for k in range(self.map_size):
            for j in range(self.map_size):
                if from_pygame[k][j].alive is False:
                    mat[k][j] = 0
                else:
                    mat[k][j] = 1
        #print(mat)
        return mat

    def set_mat(self, from_pygame):
        '''doc'''
        for i in range(self.map_size):
            for j in range(self.map_size):
                if from_pygame[i][j].alive is True:
                    self.mat[i][j] = 1
                else:
                    self.mat[i][j] = 0

    def set_mat_cell(self, from_pygame, i, j):
        '''doc'''
        if from_pygame[i][j].alive is True:
            self.mat[i][j] = 1
        else:
            self.mat[i][j] = 0


    def set_cell(self, i, j, new_value):
        '''doc'''
        self.mat[i][j] = new_value
        #self.matStr += str(self.mat)+'\n'

    def __init__(self, map_size, from_pygame):
        '''doc
        '''
        self.map_size =  map_size
        self.mat = self.start_mat(from_pygame)
        self.mat_str = ''
        self.start_file('saida.txt')

    def start_file(self, filename):
        '''doc
        '''
        file = open(filename, 'w')
        file.close()

    def save_mat(self):
        '''doc'''
        value = False
        for i in range(self.map_size):
            if 1 in self.mat[i] :
                value = True
        if value:
            self.mat_str = str(self.mat.T) + '\n'
            print(self.mat_str)
            with open('saida.txt', 'a') as file:
                file.write(self.mat_str)
