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

class Patterns():
    '''Cria as imagens dos padrões a ser procurados a partir de arrays'''
    def __init__(self, start_value):
        '''doc'''
        self.patterns = start_value
        self.rotate_dict = {'BARGE': 2,
                            'BEACON': 2,
                            'BEEHIVE': 2,
                            'BLINKER': 2,
                            'BLOCK': 1,
                            'BOAT': 4,
                            'GLIDER': 4,
                            'HALF_BAKERY': 4,
                            'HALF_FLEET': 2,
                            'LOAF': 4,
                            'LONG_BARGE': 2,
                            'LONG_BOAT': 4,
                            'MANGO': 2,
                            'POND': 1,
                            'SHIP': 2,
                            'TOAD': 2,
                            'TUB': 1}

    def rotate_patterns(self):
        for pattern_name in self.patterns:
            #if pattern_name in rotate_list:
            pattern = self.patterns[pattern_name]
            pattern_rot = self.rotate_dict[pattern_name]
            self.patterns[pattern_name] = [np.rot90(pattern, k) for k in range(pattern_rot)]
            if pattern_name == 'TOAD':
                self.patterns[pattern_name].append(np.rot90(pattern.T, 0))
                self.patterns[pattern_name].append(np.rot90(pattern.T, 1))

    def patterns_array_to_image(self):
        '''doc'''
        self.rotate_patterns()
        for pattern in self.patterns:
            for pos in enumerate(self.patterns[pattern]):
                img_path = 'data/patterns/'+pattern+str(pos[0]) +'.png'
                self.array_to_image(self.patterns[pattern][pos[0]], img_path)

    def array_to_image(self, image_array, filename):
        '''doc'''
        image_array = image_array.astype('uint8')*255
        img = Image.fromarray(image_array)
        img.save(filename)

    @property
    def patterns(self):
        '''getter de patterns'''
        return self._patterns

    @patterns.setter
    def patterns(self, start_value):
        '''seta todos os arrays que representam os padrões'''
        self._patterns = {'BLINKER': np.full([3, 5], start_value, dtype = np.bool),
                          'BLOCK': np.full([4, 4], start_value, dtype = np.bool),
                          'TUB': np.full([5, 5], start_value, dtype = np.bool),
                          'BOAT': np.full([5, 5], start_value, dtype = np.bool),
                          'GLIDER': np.full([5, 5], start_value, dtype = np.bool),
                          'SHIP': np.full([5, 5], start_value, dtype = np.bool),
                          'BEEHIVE': np.full([5, 6], start_value, dtype = np.bool),
                          'BARGE': np.full([6, 6], start_value, dtype = np.bool),
                          'TOAD': np.full([4, 6], start_value, dtype = np.bool),
                          'BEACON': np.full([6, 6], start_value, dtype = np.bool),
                          'LONG_BOAT': np.full([6, 6], start_value, dtype = np.bool),
                          'LOAF': np.full([6, 6], start_value, dtype = np.bool),
                          'POND': np.full([6, 6], start_value, dtype = np.bool),
                          'MANGO': np.full([6, 7], start_value, dtype = np.bool),
                          'LONG_BARGE': np.full([7, 7], start_value, dtype = np.bool),
                          'HALF_FLEET': np.full([8, 8], start_value, dtype = np.bool),
                          'HALF_BAKERY': np.full([9, 9], start_value, dtype = np.bool) }

        self._patterns['BLINKER'][1][1:4] = not start_value

        self._patterns['BLOCK'][1][1:3] = not start_value
        self._patterns['BLOCK'][2][1:3] = not start_value

        self._patterns['TUB'][1][2] = self._patterns['TUB'][2][1] = not start_value
        self._patterns['TUB'][2][3] = self._patterns['TUB'][3][2] = not start_value

        self._patterns['BOAT'][1][1:3] = self._patterns['BOAT'][3][2] = not start_value
        self._patterns['BOAT'][2][1] = self._patterns['BOAT'][2][3] = not start_value

        self._patterns['GLIDER'][1][1:4] = not start_value
        self._patterns['GLIDER'][2][1] = self._patterns['GLIDER'][3][2] = not start_value

        self._patterns['SHIP'][1][1:3] = self._patterns['SHIP'][2][1] = not start_value
        self._patterns['SHIP'][3][2:4] = self._patterns['SHIP'][2][3] = not start_value

        self._patterns['BEEHIVE'][1][2:4] = self._patterns['BEEHIVE'][2][1] = not start_value
        self._patterns['BEEHIVE'][3][2:4] = self._patterns['BEEHIVE'][2][4] = not start_value

        self._patterns['BARGE'][1][2] = self._patterns['BARGE'][2][1] = not start_value
        self._patterns['BARGE'][2][3] = self._patterns['BARGE'][3][2] = not start_value
        self._patterns['BARGE'][3][4] = self._patterns['BARGE'][4][3] = not start_value

        self._patterns['TOAD'][1][1:4] = self._patterns['TOAD'][2][2:5] = not start_value

        self._patterns['BEACON'][1][1:3] = self._patterns['BEACON'][2][1] = not start_value
        self._patterns['BEACON'][4][3:5] = self._patterns['BEACON'][3][4] = not start_value

        self._patterns['LONG_BOAT'][1][1:3] = self._patterns['LONG_BOAT'][2][1] = not start_value
        self._patterns['LONG_BOAT'][2][3] = self._patterns['LONG_BOAT'][3][2] = not start_value
        self._patterns['LONG_BOAT'][3][4] = self._patterns['LONG_BOAT'][4][3] = not start_value

        self._patterns['LOAF'][1][2:4] = self._patterns['LOAF'][2:4].T[1] = not start_value
        self._patterns['LOAF'][2][4] = self._patterns['LOAF'][3][3] = not start_value
        self._patterns['LOAF'][4][2] = not start_value

        self._patterns['POND'][1][2:4] = self._patterns['POND'][2:4].T[1] = not start_value
        self._patterns['POND'][4][2:4] = self._patterns['POND'][2:4].T[4] = not start_value

        self._patterns['MANGO'][1][2:4] = self._patterns['MANGO'][4][3:5] = not start_value
        self._patterns['MANGO'][2][1] = self._patterns['MANGO'][2][4] = not start_value
        self._patterns['MANGO'][3][2] = self._patterns['MANGO'][3][5] = not start_value

        self._patterns['LONG_BARGE'][1][2] = self._patterns['LONG_BARGE'][2][1] = not start_value
        self._patterns['LONG_BARGE'][2][3] = self._patterns['LONG_BARGE'][3][2] = not start_value
        self._patterns['LONG_BARGE'][3][4] = self._patterns['LONG_BARGE'][4][3] = not start_value
        self._patterns['LONG_BARGE'][4][5] = self._patterns['LONG_BARGE'][5][4] = not start_value

        self._patterns['HALF_FLEET'][1][1:3] = self._patterns['HALF_FLEET'][2][1] = not start_value
        self._patterns['HALF_FLEET'][3][2:4] = self._patterns['HALF_FLEET'][2][3] = not start_value
        self._patterns['HALF_FLEET'][4][4:6] = self._patterns['HALF_FLEET'][5][4] = not start_value
        self._patterns['HALF_FLEET'][6][5:7] = self._patterns['HALF_FLEET'][5][6] = not start_value

        self._patterns['HALF_BAKERY'][1][2:4] = not start_value
        self._patterns['HALF_BAKERY'][2][1] = not start_value
        self._patterns['HALF_BAKERY'][3][2] = not start_value
        self._patterns['HALF_BAKERY'][2:4].T[4] = not start_value
        self._patterns['HALF_BAKERY'][4][3] = not start_value
        self._patterns['HALF_BAKERY'][4][5:7] = not start_value
        self._patterns['HALF_BAKERY'][5][4] = not start_value
        self._patterns['HALF_BAKERY'][5:7].T[7] = not start_value
        self._patterns['HALF_BAKERY'][6][5] = not start_value
        self._patterns['HALF_BAKERY'][7][6] = not start_value

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
        self.file_txt = open(filename, 'w+')
        self.file_txt.truncate()
        self.file_txt.close()

    def save_mat(self):
        '''doc'''
        value = self.dead
        for i in range(self.map_size):
            if self.alive in self.mat[i] :
                value = True
        if value:
            self.mat_str = str(self.mat.T) + '\n'
            self.mat_video.append(self.mat)
            #print(self.mat_str)
            with open('saida.txt', 'a') as self.file_txt:
                self.file_txt.write(self.mat_str)
        

class FromImgToCSV():
    '''Classe que pega o array dado, transforma em imagem do tipo OpenCV e conta padrões
    '''
    def __init__(self, pattern_dict, game_of_life):
        print(game_of_life)
        self.game_of_life_video = self.start_game_of_life_video(game_of_life)
        self.game_of_life_array = game_of_life
        self.pattern_image_dict = self.start_pattern_image_dict(pattern_dict)
        index_list = [i for i in range(1, len(self.game_of_life_array)+1)]
        #print(index_list, len(self.game_of_life))
        empty_array = np.zeros(len(self.game_of_life_array))
        new_pattern_dict = {key: empty_array for key in self.pattern_image_dict}
        #print(new_pattern_dict)
        self.pattern_df = pd.DataFrame(new_pattern_dict, index = index_list)


    
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
        for frame in self.game_of_life_video:
            for pattern in self.pattern_image_dict:
                print(pattern)
                for pattern_version in self.pattern_image_dict[pattern]:
                    result = cv2.matchTemplate(frame, pattern_version, cv2.TM_CCOEFF_NORMED)
                    threshold = .6
                    loc = np.where(result >= threshold)
                    print ('loc:', loc)
