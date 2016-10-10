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
        self.alive_ptxel = start_value
        self.dead_pixel = start_value
        #1)começar um dicionario 
        self.pattern_array_dict = self.start_pattern_array_dict(patterns, start_value)
        self.game_of_life_video = self.start_game_of_life_video(game_of_life)

        self.game_of_life_array = game_of_life
        self.pattern_image_dict = self.start_pattern_image_version_dict(self.pattern_array_dict)
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
            frame_array = frame.copy().astype('uint8')*255
            #printar essas imgs geradsa
            ret,frame_img = cv2.threshold(frame_array, 0, 255, cv2.THRESH_BINARY)
            #cv2.imwrite('data/imgtest/'+ str(i) + '.png', frame_img)
            game_of_life_video.append(frame_img)
            #i+=1
        return game_of_life_video

    def start_pattern_image_version_dict(self, pattern_array_dict):
        pattern_image_dict = pattern_array_dict
        for name in pattern_image_dict:
            for k in range(len(pattern_image_dict[name])):
                pattern_image_dict[name][k] = self.start_pattern_image(pattern_array_dict, name, k)
        return pattern_image_dict
    
    def start_pattern_image(self, pattern_array_dict, pattern_name, k):
        pattern_image_array = pattern_array_dict[pattern_name][k].astype('uint8')*255
        #printar essas imgs geradas
        ret, img = cv2.threshold(pattern_image_array, 0, 255, cv2.THRESH_BINARY)
        #cv2.imwrite('data/imgtest/'+ pattern_name + str(k) + '.png',img)
        return img

    def find_patterns(self):
        for frame_number in range(0, len(self.game_of_life_video)):
            for pattern in self.pattern_image_dict:
                amnt_matches = 0
                #print(pattern)
                #k=0
                for pattern_version in self.pattern_image_dict[pattern]:
                    
                    amnt_matches = self.crop_borders(pattern_version, self.game_of_life_video[frame_number])
                    #k+=1
                    #print(amnt_matches)
                    self.pattern_df[pattern][frame_number] += amnt_matches
        print(self.pattern_df)
        

    def get_amnt_matches(self, frame, pattern_image_version):
        #print(frame)
        pt_height,pt_width = pattern_image_version.shape
        f_height, f_width = frame.shape
        #print(pt_height, pt_width, f_height, f_width)
        if 0 not in (pt_height, f_height, pt_width, f_width):
            if (f_height > pt_height) and (f_width > pt_width):
                result = cv2.matchTemplate(frame, pattern_image_version, cv2.TM_CCOEFF_NORMED)
                threshold= .778
                count = len(np.where(result >= threshold)[0]) + len(np.where(result <= -threshold)[0])
                return count
            else:
                return 0
        else:
            #print('tem 0')
            return 0
        return 0
        #print('afdsklça')
                    
    def crop_borders(self, pattern_image_version, frame):
        amnt_matches = 0
        pt_height,pt_width = pattern_image_version.shape
        f_height, f_width = frame.shape
        #print(pt_height, pt_width, f_height, f_width)
        #no meio:
        #cv2.imwrite('data/imgtest/' + str(frame_number) +'.png',frame)
        amnt_matches += self.get_amnt_matches(frame, pattern_image_version)
        
        
        #Área 1)
        pattern_image_version_crop_1 = pattern_image_version[1:, 1:]
        frame_1 = frame[:pt_height, :pt_width]
        #print(pt_height, frame_1.shape[0])
        #cv2.imwrite('data/imgtest/' + str(frame_number) +'_1.png',frame_1)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) + '_1.png',pattern_image_version_crop_1)
        #print(frame_1, '\n', pattern_image_version_crop_1)
        amnt_matches += self.get_amnt_matches(frame_1, pattern_image_version_crop_1) 
        
        #Área 2)
        pattern_image_version_crop_2 = pattern_image_version[1:, :]
        frame_2 = frame[:pt_height, pt_width:f_width-pt_width]
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_2.png',frame_2)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_2.png',pattern_image_version_crop_2)
        
        amnt_matches += self.get_amnt_matches(frame_2, pattern_image_version_crop_2) 
        
        #Área 3)
        pattern_image_version_crop_3 = pattern_image_version[1:, :pt_width-1]
        frame_3 = frame[:pt_height, f_width - pt_width:]
        amnt_matches += self.get_amnt_matches(frame_3, pattern_image_version_crop_3) 
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_3.png',frame_3)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_3.png',pattern_image_version_crop_3)
        
        #Área 4)
        pattern_image_version_crop_4 = pattern_image_version[:, :pt_width-1]
        frame_4 = frame[pt_height:f_height-pt_height, f_width-pt_width:]
        amnt_matches += self.get_amnt_matches(frame_4, pattern_image_version_crop_4) 
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_4.png',frame_4)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_4.png',pattern_image_version_crop_4)
        
        
        #Área 5)
        pattern_image_version_crop_5 = pattern_image_version[:pt_height-1, :pt_width-1]
        frame_5 = frame[f_height-pt_height:, f_width-pt_width:]
        amnt_matches += self.get_amnt_matches(frame_5, pattern_image_version_crop_5) 
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_5.png',frame_5)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_5.png',pattern_image_version_crop_5)
        
        #Área 6)
        pattern_image_version_crop_6 = pattern_image_version[:pt_height-1, :]
        frame_6 = frame[f_height-pt_height:f_height, pt_width:f_width-pt_width]
        amnt_matches += self.get_amnt_matches(frame_6, pattern_image_version_crop_6) 
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_6.png',frame_2)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_6.png',pattern_image_version_crop_6)
        
        #Área 7)
        pattern_image_version_crop_7 = pattern_image_version[:pt_height-1, 1:]
        frame_7 = frame[f_height-pt_height:, :pt_width]
        amnt_matches += self.get_amnt_matches(frame_7, pattern_image_version_crop_7) 
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_7.png',frame_7)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_7.png',pattern_image_version_crop_7)
        
        #Área 8)
        pattern_image_version_crop_8 = pattern_image_version[:, 1:]
        frame_8 = frame[pt_height:f_height - pt_height, :pt_width]
        amnt_matches += self.get_amnt_matches(frame_8, pattern_image_version_crop_8)
        #cv2.imwrite('data/imgtest/' + str(frame_number)  + '_8.png',frame_8)
        #cv2.imwrite('data/imgtest/' + pattern_name + str(k) +'_8.png',pattern_image_version_crop_8)
        
        return amnt_matches 
    
    def save_csv(self, name):
        self.pattern_df.to_csv('data/files/csv/'+ name, encoding = 'utf8', sep = ';')