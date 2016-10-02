#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2016

@author: Nicoli
'''

from collections import OrderedDict
import random
import pygame
from pygame.locals import *

from PatternsParser import Patterns

class Cell:
    '''Célula da imagem que vai ser formada.
    '''
    def __init__(self, location, alive = False): #ESTADO DA CELULA COMECA MORTO (FALSE)
        '''Cada célula é iniciada morta, sem estar pressionada e com a localização informada.
            to_be: é o próximo estado da célula
            alive (bool): pode ser True (caso viva) ou False (caso morta).
            A inicialização padrão assume que a célula está morta, mas caso o campo alive
            estiver preenchido com True na declaração, a célula é inicializada viva.
            pressed (bool): a célula está pressionada pelo mouse?
            locatio: localização da célula na imagem
        '''

        self.to_be = None
        self.alive = alive
        self.pressed = False
        self.location = location

    def set_alive(self, alive):
        '''setter do alive'''
        self.alive = alive

    def set_to_be(self, to_be):
        '''setter do to_be'''
        self.to_be = to_be

    def set_pressed(self, pressed):
        '''setter do pressed'''
        self.pressed = pressed

    def set_location(self, location):
        '''setter do location'''
        self.location = location


class Board:
    '''Maniputa tudo que tem a ver com o quadro do jogo
    '''

    def __init__(self, squares, map_size, speed):
        '''
        squares: tamanho das células ==> 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
        speed: quantas iterações ocorrerão por segundo
        map: list [squares x squares] com os valores dos pixeis
        cell_img: lista que armazena o local de cada imagem que representará a célula
        viva, morta e quantos pixeis essa imagem terá
        alive_img abre a imagem e a converte pra uma tela do pygame
        '''
        self.speed = speed
        self.map_size = map_size
        self.map = []
        self.cell_img = self.set_squares(squares)
        width = self.map_size*self.cell_img[2]
        height = self.map_size*self.cell_img[2]
        screen_size = width, height
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.alive_img = pygame.image.load(self.cell_img[0]).convert() 
        self.dead_img = pygame.image.load(self.cell_img[1]).convert()
        self.done = False
    
        self.fill(False)
        self.t_p = 0
        self.run = False
        self.parser = Patterns(self.map_size, self.map)
        #self.parser.setMat(self.map)

    def set_squares(self, squares):
        '''Imagem que representa cada célula em seus estados viva e morta de acordo com seu tamanho
        retorna uma lista tal que:
        img = [img[0], img[1], img[2]]
            img[0] = caminho para imagem de uma célula viva
            img[1] = caminho para imagem de uma célula morta
            img[2] = qtd de pixels por imagem
        '''
        if squares == 0:
            img = ["res/alive_8.png", "res/dead_8.png", 8]
        elif squares == 1:
            img = ["res/alive_16.png", "res/dead_16.png", 16]
        if squares == 2:
            img = ["res/alive_32.png", "res/dead_32.png", 32]
        if squares == 3:
            img = ["res/alive_64.png", "res/dead_64.png", 64]
        return img

    def fill(self,rand_bool):
        '''dfjsa
        '''
        for line in range(self.map_size):
            self.map.append([])
            for column in range(self.map_size):
                if rand_bool is True:
                    rand_number = random.randint(0,4)
                    if rand_number == 0:
                        self.map[line].insert(column,Cell((line,column),True))
                    else:
                        self.map[line].insert(column,Cell((line,column)))
                else: self.map[line].insert(column,Cell((line,column)))


    def draw(self):
        '''sdfj
        '''
        for line in range(self.map_size):
            for column in range(self.map_size):
                cell = self.map[line][column]
                size = self.cell_img[2]
                loc = cell.location
                if cell.alive is True:
                    self.screen.blit(self.alive_img,(loc[0]*size,loc[1]*size))
                else:
                    self.screen.blit(self.dead_img,(loc[0]*size,loc[1]*size))

    def get_cells(self, Cell):# gets the Cells around a Cell
        '''method doc
        '''
        mapa = self.map
        list_a = []
        list_b = []
        int_count = 0
        cell_loc = Cell.location
        try:
            list_a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
        except Exception:
            pass
        try:
            list_a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
        except Exception:
            pass
        #num = len(list(OrderedDict.fromkeys(a)))# removes duplicates
        for line in range(len(list_a)): list_b.append(mapa[list_a[line][0]][list_a[line][1]].alive)
        for line in list_b:# c houses how many Cells are alive around it
            if line is True:
                int_count+=1
        if Cell.alive is True:# rules
            if int_count < 2:
                Cell.to_be = False
            if int_count > 3:
                Cell.to_be = False
        elif int_count == 3:
            Cell.to_be = True

    def update_frame(self):
        '''doc
        '''
        for line in range(self.map_size):
            for column in range(self.map_size):
                cell = self.map[line][column]
                self.get_cells(cell)
                self.parser.setMatCell(self.map, line, column)

    def update(self):
        '''doc
        '''
        for line in range(self.map_size):
            for column in range(self.map_size):
                cell = self.map[line][column]
                size = self.cell_img[2]
                loc = cell.location
                if cell.to_be is not None:
                    cell.alive = cell.to_be
                if self.map[line][column].alive is True:
                    self.screen.blit(self.alive_img,(loc[0]*size,loc[1]*size))
                else:
                    self.screen.blit(self.dead_img,(loc[0]*size,loc[1]*size))
                cell.to_be = None

    def set_board(self):
        '''doc
        '''
        while self.done is False:
            milliseconds = self.clock.tick(60)
            #seconds = milliseconds / 1000.0
            self.t_p += milliseconds

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.run = not self.run

                if event.type == KEYUP:
                    if event.key == K_q:
                        self.run = False
                        self.update_frame()
                        self.update()

                if event.type == MOUSEBUTTONUP:
                    for line in range(self.map_size):
                        for column in range(self.map_size):
                            self.map[line][column].pressed = False


            pressed = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()

            if pressed[K_KP0]:
                self.map[0][0].alive = True
                self.update()

            if pressed[K_KP2]:
                self.parser.setMat(self.map)


            if pressed[K_r]:
                self.map = []
                self.fill(False)
                self.draw()
            
            if pressed[K_a]:
                self.map = []
                self.fill(True)
                self.draw()

            if self.run is True and self.t_p >= 1000/self.speed :
                self.t_p = 0
                self.parser.saveMat()
                self.update_frame()
                self.update()

            if mouse[0]:# makes Cells alive
                rects = self.get_cell_list()
                for line in range(self.map_size):
                    for column in range(self.map_size):
                        if pos[0] >= rects[line][column][0] and pos[0] < rects[line][column][0]+self.cell_img[2]:
                            if pos[1] >= rects[line][column][1] and pos[1] < rects[line][column][1]+self.cell_img[2]:
                                if self.map[line][column].pressed is False:
                                    self.map[line][column].alive = True
                                    self.parser.setCell(line, column, 1)
                                    self.map[line][column].pressed = True
                                    self.update()

            if mouse[2]: # kills Cells
                rects = self.get_cell_list()
                size = self.cell_img[2]
                for line in range(self.map_size):
                    for col in range(self.map_size):
                        if pos[0] >= rects[line][col][0] and pos[0]<rects[line][col][0]+size:
                            if pos[1]>=rects[line][col][1] and pos[1]<rects[line][col][1]+size:
                                if self.map[line][col].pressed is False:
                                    self.map[line][col].alive = False
                                    self.map[line][col].pressed = False
                                    self.parser.setCell(line, col, 0)
                                    self.update()

            pygame.display.flip()

    def get_cell_list(self):
        '''doc
        '''
        cell_list = []
        size = self.cell_img[2]
        for line in range(self.map_size):
            cell_list.append([])
            for column in range(self.map_size):
                cell = self.map[line][column]
                cell_list[line].append((cell.location[0]*size,cell.location[1]*size))
        return cell_list
