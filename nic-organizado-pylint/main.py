#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Módulo Main:
'''
#from collections import OrderedDict
#import pygame, random
#from pygame.locals import *
from Game import Board
from PatternsParser import Patterns, FromImgToCSV
#from PatternsParser import Patterns

if __name__ == '__main__':
    SPEED = 1
    SQUARES = 2
    MAP_SIZE = 8
    START_VALUE = True
    NEW_BOARD = Board(SQUARES, MAP_SIZE, START_VALUE)
    NEW_BOARD.set_board(SPEED)
    NEW_PATTERNS = Patterns(START_VALUE)
    NEW_PATTERNS.rotate_patterns()
    #NEW_PATTERNS.patterns_array_to_image()
    NEW_PARSER = FromImgToCSV(NEW_PATTERNS.patterns, NEW_BOARD.parser.mat_video)
    NEW_PARSER.find_patterns()
