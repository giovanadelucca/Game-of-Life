#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pylint: disable=redefined-outer-name
#pylint: disable=attribute-defined-outside-init
#pylint: disable=undefined-variable
#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-nested-blocks
#pylint: disable=too-many-branches
'''
Created on Oct 1, 2016

@author: Nicoli
'''

#from collections import OrderedDict
import random
import pygame
from pygame.locals import *

from PatternsParser import GameArrayParser

class Cell:
    '''Célula da imagem que vai ser formada.
    '''
    def __init__(self, location, alive=False): #ESTADO DA CELULA COMECA MORTO (FALSE)
        '''Cada célula é iniciada morta, sem estar pressionada e com a localização informada.
            to_be: é o próximo estado da célula
            alive (bool): pode ser True (caso viva) ou False (caso morta).
            A inicialização padrão assume que a célula está morta, mas caso o campo alive
            estiver preenchido com True na declaração, a célula é inicializada viva.
            pressed (bool): a célula está pressionada pelo mouse?
            locatio: localização da célula na imagem
        '''

        self._to_be = None
        self._alive = alive
        self._pressed = False
        self._location = location

    @property
    def alive(self):
        '''getter do alive'''
        return self._alive

    @alive.setter
    def alive(self, alive):
        '''setter do alive'''
        self._alive = alive

    @property
    def to_be(self):
        '''getter do to_be'''
        return self._to_be

    @to_be.setter
    def to_be(self, to_be):
        '''setter do to_be'''
        self._to_be = to_be

    @property
    def pressed(self):
        '''getter do pressed'''
        return self._pressed

    @pressed.setter
    def pressed(self, pressed):
        '''setter do pressed'''
        self._pressed = pressed

    @property
    def location(self):
        '''geter do location'''
        return self._location

    @location.setter
    def set_location(self, location):
        '''setter do location'''
        self._location = location

class Board:
    '''Manipula tudo que tem a ver com o quadro do jogo
    '''

    def __init__(self, squares, map_size, start_value, generations):
        '''
        squares: tamanho das células ==> 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
        map: list [squares x squares] com os valores dos pixeis
        cell_img: lista que armazena o local de cada imagem que representará a célula
        viva, morta e quantos pixeis essa imagem terá
        '''
        self.generations = generations
        self.count_gen = 0
        self._map_size = map_size
        self.map = []
        self.cell_img = squares
        self.fill(False)
        self.parser = GameArrayParser(self.map_size, self.map, start_value)
        self.screen = [self.map_size, self.cell_img[2]]
        self.alive_img = self.cell_img[0]
        self.dead_img = self.cell_img[1]

    @property
    def map_size(self):
        '''getter do map_size'''
        return self._map_size

    @map_size.setter
    def map_size(self, map_size):
        '''setter do map_size'''
        self._map_size = map_size

    @property
    def map(self):
        '''getter do map'''
        return self._map

    @map.setter
    def map(self, map_value):
        '''setter do map'''
        self._map = map_value

    @property
    def cell_img(self):
        '''getter do cell_img'''
        return self._cell_img

    @cell_img.setter
    def cell_img(self, squares):
        '''Imagem que representa cada célula em seus estados viva e morta de acordo com seu tamanho
        retorna uma lista tal que:
        img = [img[0], img[1], img[2]]
            img[0] = caminho para imagem de uma célula viva
            img[1] = caminho para imagem de uma célula morta
            img[2] = qtd de pixels por imagem
        '''
        if squares == 0:
            self._cell_img = ["data/cell_image/alive_8.png", "data/cell_image/dead_8.png", 8]
        elif squares == 1:
            self._cell_img = ["data/cell_image/alive_16.png", "data/cell_image/dead_16.png", 16]
        elif squares == 2:
            self._cell_img = ["data/cell_image/alive_32.png", "data/cell_image/dead_32.png", 32]
        elif squares == 3:
            self._cell_img = ["data/cell_image/alive_64.png", "data/cell_image/dead_64.png", 64]

    @property
    def parser(self):
        '''getter do parser'''
        return self._parser

    @parser.setter
    def parser(self, parser):
        '''setter do parser'''
        self._parser = parser

    @property
    def alive_img(self):
        '''getter do alive_img'''
        return self._alive_img

    @alive_img.setter
    def alive_img(self, alive_img_path):
        '''setter do alive_img'''
        self._alive_img = pygame.image.load(alive_img_path).convert()

    @property
    def dead_img(self):
        '''getter do dead_img'''
        return self._dead_img

    @dead_img.setter
    def dead_img(self, dead_img_path):
        '''setter do dead_img'''
        self._dead_img = pygame.image.load(dead_img_path).convert()

    @property
    def screen(self):
        '''getter de screen'''
        return self._screen

    @screen.setter
    def screen(self, param_list):
        '''setter de screen'''
        map_size = param_list[0]
        pixel_size = param_list[1]
        width = map_size*pixel_size
        height = map_size*pixel_size
        screen_size = width, height
        self._screen = pygame.display.set_mode(screen_size)

    def fill(self, rand_bool):
        '''DOCUMENTAR
        '''
        for line in range(self.map_size):
            self.map.append([])
            for column in range(self.map_size):
                if rand_bool is True:
                    rand_number = random.randint(0, 4)
                    if rand_number == 0:
                        self.map[line].insert(column, Cell((line, column), True))
                    else:
                        self.map[line].insert(column, Cell((line, column)))
                else: self.map[line].insert(column, Cell((line, column)))

    def draw(self):
        '''DOCUMENTAR
        '''

        for line in range(self.map_size):
            for column in range(self.map_size):
                cell = self.map[line][column]
                size = self.cell_img[2]
                loc = cell.location
                if cell.alive is True:
                    self.screen.blit(self.alive_img, (loc[0]*size, loc[1]*size))
                else:
                    self.screen.blit(self.dead_img, (loc[0]*size, loc[1]*size))

    def get_cells(self, cell):# gets the Cells around a Cell
        '''Regra do autômato'''
        mapa = self.map
        list_a = []
        list_b = []
        int_count = 0
        cell_loc = cell.location
        try:
            list_a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
        except IndexError:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
        except IndexError:
            pass
        #num = len(list(OrderedDict.fromkeys(a)))# removes duplicates

        for item in enumerate(list_a):
            list_b.append(mapa[item[1][0]][item[1][1]].alive)
        for line in list_b:# c houses how many Cells are alive around it
            if line is True:
                int_count += 1
        if cell.alive is True:# rules
            if int_count < 2:
                cell.to_be = False
            if int_count > 3:
                cell.to_be = False
        elif int_count == 3:
            cell.to_be = True

    def update_frame(self):
        '''DOCUMENTAR'''
        self.count_gen+=1
        for line in range(self.map_size):
            for column in range(self.map_size):
                cell = self.map[line][column]
                self.get_cells(cell)
                #
        self.parser.update_mat(self.map)


    def update(self):
        '''DOCUMENTAR
        '''
        for line in range(self.map_size):
            for column in range(self.map_size):
                cell = self.map[line][column]
                size = self.cell_img[2]
                loc = cell.location
                if cell.to_be is not None:
                    cell.alive = cell.to_be
                if self.map[line][column].alive is True:
                    self.screen.blit(self.alive_img, (loc[0]*size, loc[1]*size))
                else:
                    self.screen.blit(self.dead_img, (loc[0]*size, loc[1]*size))
                cell.to_be = None
        #self.parser.update_mat(self.map)
        self.parser.mat = self.map
        #print(self.parser.mat)
        #print(self.map)
   

    def set_board(self, speed):
        '''DOCUMENTAR
        '''
        clock = pygame.time.Clock()
        done = False
        t_p = 0
        run = False
        size = self.cell_img[2]
        while done is False:
            milliseconds = clock.tick(60)
            #seconds = milliseconds / 1000.0
            t_p += milliseconds

            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                    
                    #self.parser.save_mat()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        run = not run


                if event.type == KEYUP:
                    if event.key == K_q:
                        run = False
                        self.update_frame()
                        self.update()
                        
                #se apertar pra cima, fica limpo
                if event.type == MOUSEBUTTONUP:
                    for line in range(self.map_size):
                        for column in range(self.map_size):
                            self.map[line][column].pressed = False
                            #self.parser.update_mat(self.map)


            pressed = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()

            if pressed[K_KP0]: #se 0 for apertado, a célula 0 0 fica viva
                self.map[0][0].alive = True
                self.parser.mat = self.map
                self.parser.set_mat()
                self.update()

            if pressed[K_KP2]: #se apertar 2, salva a matriz
                self.parser.mat = self.map
                #self.parser.update_mat()

            if pressed[K_r]: #se apertar o r, reinicia a tela com false
                self.map = []
                self.fill(False)
                self.draw()
                

            if pressed[K_a]: #se apertar o a, reinicia a tela com true
                self.map = []
                self.fill(True)
                self.draw()

            if run is True and t_p >= 1000/speed and self.count_gen<=self.generations:
                t_p = 0
                
                self.update_frame()
                self.update()
                #self.parser.update()

            if mouse[0]:# makes Cells alive
                rects = self.get_cell_list()
                for line in range(self.map_size):
                    for col in range(self.map_size):
                        if pos[0] >= rects[line][col][0] and pos[0] < rects[line][col][0]+size:
                            if pos[1] >= rects[line][col][1] and pos[1] < rects[line][col][1]+size:
                                if self.map[line][col].pressed is False:
                                    self.map[line][col].alive = True
                                    #self.parser.set_cell(line, col, 1)
                                    self.map[line][col].pressed = True
                                    self.update()

            if mouse[2]: # kills Cells
                rects = self.get_cell_list()
                for line in range(self.map_size):
                    for col in range(self.map_size):
                        if pos[0] >= rects[line][col][0] and pos[0] < rects[line][col][0]+size:
                            if pos[1] >= rects[line][col][1] and pos[1] < rects[line][col][1]+size:
                                if self.map[line][col].pressed is False:
                                    self.map[line][col].alive = False
                                    self.map[line][col].pressed = False
                                    self.parser.set_cell(line, col, 0)
                                    self.update()
            
            pygame.display.flip()

    def get_cell_list(self):
        '''DOCUMENTAR
        '''
        cell_list = []
        size = self.cell_img[2]
        for line in range(self.map_size):
            cell_list.append([])
            for column in range(self.map_size):
                cell = self.map[line][column]
                cell_list[line].append((cell.location[0]*size, cell.location[1]*size))
        return cell_list
