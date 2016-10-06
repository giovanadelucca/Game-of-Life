#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pylint: disable=redefined-outer-name
#pylint: disable=attribute-defined-outside-init
#pylint: disable=undefined-variable
#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-nested-blocks
#pylint: disable=too-many-branches
#pylint: disable=no-member
'''
Nicoli
'''
import cv2
import numpy as np
from PIL import Image
import pandas as pd

class GameArrayParser():
    '''doc
    '''
    @property
    def mat(self):
        '''getter de mat
        '''
        return self._mat

    @mat.setter
    def mat(self, from_pygame):
        '''doc'''
        for i in range(self.map_size):
            for j in range(self.map_size):
                if from_pygame[i][j].alive is True:
                    self._mat[i][j] = self.alive
                else:
                    self._mat[i][j] = self.dead

    def set_mat_cell(self, from_pygame, i, j):
        '''doc'''
        if from_pygame[i][j].alive is True:
            self._mat[i][j] = self.alive
        else:
            self._mat[i][j] = self.dead

    def set_cell(self, i, j, new_value):
        '''doc'''
        self._mat[i][j] = new_value
        #self.matStr += str(self.mat)+'\n'

    def __init__(self, map_size, from_pygame, start_value):
        '''doc
        '''
        self.dead = start_value
        self.alive = not start_value
        self.map_size =  map_size
        self._mat = np.full([self.map_size, self.map_size], self.dead, dtype = np.bool)
        self.mat = from_pygame
        self.mat_video = [self.mat]
        self.mat_str = ''
        self.start_file_txt('data/files/saida.txt')
 
    #@property
    def start_file_txt(self, filename):
        '''setter de file_txt'''
        self.file_txt = open(filename, 'w')
        self.file_txt.truncate()
        self.file_txt.close()

    def save_mat(self):
        '''doc'''
        value = self.dead
        for i in range(self.map_size):
            if self.alive in self.mat[i] :
                value = True
        if value:
            self.mat_str = str(self.mat) + '\n'
            self.mat_video.append(self.mat)
            #print(self.mat_str)
            with open('saida.txt', 'a') as self.file_txt:
                self.file_txt.write(self.mat_str)
        

class FromImgToCSV():
    '''Classe que pega o array dado, transforma em imagem do tipo OpenCV e conta padrões
    '''
    def __init__(self, pattern_dict, game_of_life):
        #print(game_of_life)
        self.game_of_life_video = self.start_game_of_life_video(game_of_life)
        self.start_pattern_count_dict(pattern_dict, len(game_of_life[0]))
        #self.pattern_count_dict = pattern_dict
        self.game_of_life_array = game_of_life
        self.pattern_image_dict = self.start_pattern_image_dict(pattern_dict)
        index_list = [i for i in range(0, len(self.game_of_life_array))]
        #print(index_list, len(self.game_of_life))
        empty_array = np.zeros(len(self.game_of_life_array))
        new_pattern_dict = {key: empty_array for key in self.pattern_image_dict}
        #print(new_pattern_dict)
        self.pattern_df = pd.DataFrame(new_pattern_dict, index = index_list)

    def start_pattern_count_dict(self, pattern_dict, size):
        self.pattern_count_dict = {}
        for key in pattern_dict:
            self.pattern_count_dict[key] = np.full([size], 0, np.int32)

    
    def start_game_of_life_video(self, game_of_life_array):
        game_of_life_video = []
        for frame in game_of_life_array:
            frame_array = frame.astype('uint8')*255
            frame_img = cv2.adaptiveThreshold(frame_array, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
            game_of_life_video.append(frame_img)
        return game_of_life_video

    def start_pattern_image_dict(self, pattern_array_dict):
        pattern_image_dict = pattern_array_dict
        for name in pattern_image_dict:
            for k in range(len(pattern_image_dict[name])):
                pattern_image_dict[name][k] = self.start_pattern_image(pattern_array_dict, name, k)
        return pattern_image_dict
    
    def start_pattern_image(self, pattern_array_dict, pattern_name, k):
        pattern_image_array = pattern_array_dict[pattern_name][k].astype('uint8')*255
        return cv2.adaptiveThreshold(pattern_image_array, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)

    def find_patterns(self):
        for frame in range(0, len(self.game_of_life_video)):
            for pattern in self.pattern_image_dict:
                count_pattern = 0
                #print(pattern)
                for pattern_version in self.pattern_image_dict[pattern]:
                    result = cv2.matchTemplate(self.game_of_life_video[frame], pattern_version, cv2.TM_CCOEFF_NORMED)
                    threshold = 1
                    result = np.where(result >= threshold)
                    count_pattern += len(result[1])
                    #print ('loc:', len(loc[1]))
                print(self.pattern_count_dict[pattern][frame], pattern, frame)
                self.pattern_count_dict[pattern][frame] = count_pattern
                print(self.pattern_count_dict)
