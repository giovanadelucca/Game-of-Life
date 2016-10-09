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
        from_pygame = np.asarray(from_pygame).T
        for i in range(self.map_size):
            for j in range(self.map_size):
                if from_pygame[j][i].alive is True:
                    self._mat[j][i] = self.alive
                else:
                    self._mat[j][i] = self.dead
        
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
        '''doc'''
        self.dead = start_value
        self.alive = not start_value
        self.map_size =  map_size
        self._mat = np.full([self.map_size, self.map_size], self.dead, dtype = np.bool)
        self.mat = from_pygame
        self.mat_video = [self.mat.copy()]
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
        '''value = self.dead
        for i in range(self.map_size):
            if self.alive in self.mat[i] :
                value = True
        if value:
            self.mat_str = str(self.mat) + '\n'
            self.mat_video.append(self.mat)
            #print(self.mat_str)
            with open('saida.txt', 'a') as self.file_txt:
                self.file_txt.write(self.mat_str)'''
        self.mat_video.append(self.mat)
        
    def update_mat(self, from_pygame):
        
        self.mat = from_pygame
        #print(self.mat)
        #print('\n')
        self.mat_video.append(self.mat.copy())

class FromImgToCSV():
    '''Classe que pega o array dado, transforma em imagem do tipo OpenCV e conta padrões
    '''
    def __init__(self, start_value, patterns, game_of_life):
        self.alive_pixel = start_value
        self.dead_pixel = start_value
        #1)começar um dicionario 
        self.pattern_array_dict = self.start_pattern_array_dict(patterns, start_value)
        self.game_of_life_video = self.start_game_of_life_video(game_of_life)

        self.game_of_life_array = game_of_life
        self.pattern_image_dict = self.start_pattern_image_dict(self.pattern_array_dict)
        index_list = [i for i in range(0, len(self.game_of_life_array))]

        empty_array = np.zeros(len(self.game_of_life_array))
        new_pattern_dict = {key: empty_array for key in self.pattern_image_dict}

        self.pattern_df = pd.DataFrame(new_pattern_dict, index = index_list)
    @property
    def alive_pixel(self):
        return self._alive_pixel
    
    @alive_pixel.setter
    def alive_pixel(self, start_value):
        if start_value == False:
            self._alive_pixel = 0
        elif start_value == True:
            self._alive_pixel = 255
            
    @property
    def dead_pixel(self):
        return self._alive_pixel
    
    @alive_pixel.setter
    def dead_pixel(self, start_value):
        if start_value == False:
            self._dead_pixel = 0
        elif start_value == True:
            self._dead_pixel = 255
    def start_pattern_array_dict(self, patterns, start_value):
        pattern_dict_array = {}
        for p in patterns:
            pattern_dict_array[p] = []
            for rot in range(4):
                try:
                    if str(start_value) == 'True':
                        txtpath = 'data/patterns/txt/True/'+p+str(rot) +'.txt'
                    elif str(start_value) == 'False':
                        txtpath = 'data/patterns/txt/False/'+p+str(rot) +'.txt'
                    #print(p, rot)
                    pattern_dict_array[p].append(np.loadtxt(txtpath, delimiter=' '))
                except FileNotFoundError:
                    pass
        #print(pattern_dict_array)
        return pattern_dict_array

    def start_game_of_life_video(self, game_of_life_array):
        game_of_life_video = []
        i=0
        for frame in game_of_life_array:
            frame_array = frame.astype('uint8')*255
            #print(frame)
            #print(frame_array)
            #printar essas imgs geradsa
            ret,frame_img = cv2.threshold(frame_array, 0, 255, cv2.THRESH_BINARY)
            cv2.imwrite('data/imgtest/'+ str(i) + '.png', frame_img)
            game_of_life_video.append(frame_img)
            i+=1
        return game_of_life_video

    def start_pattern_image_dict(self, pattern_array_dict):
        pattern_image_dict = pattern_array_dict
        for name in pattern_image_dict:
            for k in range(len(pattern_image_dict[name])):
                pattern_image_dict[name][k] = self.start_pattern_image(pattern_array_dict, name, k)
        return pattern_image_dict
    
    def start_pattern_image(self, pattern_array_dict, pattern_name, k):
        pattern_image_array = pattern_array_dict[pattern_name][k].astype('uint8')*255
        #printar essas imgs geradas
        ret, img = cv2.threshold(pattern_image_array, 0, 255, cv2.THRESH_BINARY)
        cv2.imwrite('data/imgtest/'+ pattern_name + str(k) + '.png',img)
        return img

    def find_patterns(self):
        for frame in range(0, len(self.game_of_life_video)):
            for pattern in self.pattern_image_dict:
                count_pattern = 0
                for pattern_version in self.pattern_image_dict[pattern]:
                    
                    #print(pattern, len(result[1]))
                self.pattern_df[pattern][frame] += len(result[1])
        print(self.pattern_df)
        self.pattern_df.to_csv('data/files/csv/teste.csv', encoding = 'utf8')

    def get_amnt_matches(self, frame, pattern):
        result = cv2.matchTemplate(self.game_of_life_video[frame], pattern_version, cv2.TM_CCOEFF_NORMED)
        threshold = 1
        return len(np.where(result >= threshold))
                    
    def crop_borders(self, pattern_image, frame):
        amnt_matches = 0
        pi_height,pi_width = pattern_image.shape
        f_height, f_width = frame.shape
        #1)
        pattern_image_crop_1 = pattern_image[1:pi_height, 1:pi_width]
        frame_1 = frame[0:pi_height, 0:pi_width]
        amnt_matches += self.get_amnt_matches(frame_1, pattern_image_crop_1) 
        #2)
        pattern_image_crop_2 = pattern_image[1:pi_height, 0:pi_width]
        frame_2 = frame[0:pi_height-1, pi_width:f_width-pi_width]
        amnt_matches += self.get_amnt_matches(frame_2, pattern_image_crop_2) 
        
        #6)
        pattern_image_crop_2 = pattern_image[1:pi_height, 0:pi_width]
        frame_2 = frame[0:pi_height-1, pi_width:f_width-pi_width]
        amnt_matches += self.get_amnt_matches(frame_2, pattern_image_crop_2) 
        