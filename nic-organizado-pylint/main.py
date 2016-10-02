#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Main
'''
#from collections import OrderedDict
#import pygame, random
#from pygame.locals import *
from Game import Board
#from PatternsParser import Patterns

if __name__ == '__main__':
    SPEED = 0.5
    SQUARES = 1
    MAP_SIZE = 8
    new_board = Board(SQUARES, MAP_SIZE, SPEED) 
    new_board.setBoard()

    