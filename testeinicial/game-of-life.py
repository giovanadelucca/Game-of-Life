from collections import OrderedDict
import pygame
import pygame,random
from pygame.locals import *

speed = 10 # how many iterations per second

# size of squares 
square_size = 16 # width and height

# board size 
board_size = 64 # width and height

# assets folder name
assets_folder = 'assets/'

# assets that represents each cell (alive and dead) by size

assets_dictionary = {
  8: (assets_folder + 'alive_08.png', assets_folder + 'dead_08.png'),
  16: (assets_folder + 'alive_16.png', assets_folder + 'dead_16.png'),
  32: (assets_folder + 'alive_32.png', assets_folder + 'dead_32.png'),
  64: (assets_folder + 'alive_64.png', assets_folder + 'dead_64.png')
}

alive_image, dead_image = assets_dictionary[square_size]

# configuration

width = board_size*square_size
height = board_size*square_size
screen_size = width, height
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
alive = pygame.image.load(alive_image).convert()
dead = pygame.image.load(dead_image).convert()
done = False

class cell:

    def __init__(self, location, alive = False): #ESTADO DA CELULA COMECA MORTO (FALSE)
        self.to_be = None
        self.alive = alive
        self.pressed = False
        self.location = location


class board:

    def __init__(self):
        self.map = []

    def fill(self, ran):
        for i in range(board_size):
            self.map.append([])
            for g in range(board_size):
                if ran == True:
                    a = random.randint(0,4)
                    if a == 0: self.map[i].insert(g,cell((i,g),True))
                    else: self.map[i].insert(g,cell((i,g)))    
                else: self.map[i].insert(g,cell((i,g)))
                    

    def draw(self):
        for i in range(board_size):
            for g in range(board_size):
                cell = self.map[i][g]
                loc = cell.location
                if cell.alive == True: screen.blit(alive,(loc[0]*square_size,loc[1]*square_size))
                else: screen.blit(dead,(loc[0]*square_size,loc[1]*square_size))

    def get_cells(self,cell):# gets the cells around a cell
        mapa = self.map
        a = []
        b = []
        c = 0
        cell_loc = cell.location
        try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
        except Exception: pass
        num = len(list(OrderedDict.fromkeys(a)))# removes duplicates
        for i in range(len(a)): b.append(mapa[a[i][0]][a[i][1]].alive)
        for i in b:# c houses how many cells are alive around it
            if i == True: c+=1
        if cell.alive == True:# rules
            if c < 2: cell.to_be = False
            if c > 3:cell.to_be = False
        else:
            if c == 3: cell.to_be = True
                              #rules
    def update_frame(self):
        for i in range(board_size):
            for g in range(board_size):
                cell = self.map[i][g]
                self.get_cells(cell)

    def update(self):
        for i in range(board_size):
            for g in range(board_size):
                cell = self.map[i][g]
                loc = cell.location
                if cell.to_be != None: cell.alive = cell.to_be
                if self.map[i][g].alive == True: screen.blit(alive,(loc[0]*square_size,loc[1]*square_size))
                else: screen.blit(dead,(loc[0]*square_size,loc[1]*square_size))
                cell.to_be = None

def cell_list():
    lst = []
    for i in range(board_size):
        lst.append([])
        for g in range(board_size): lst[i].append((board.map[i][g].location[0]*square_size,board.map[i][g].location[1]*square_size))
    return lst

########################
board = board()
board.fill(False)
board.draw()  
tp = 0
run = False

while done == False:
    milliseconds = clock.tick(60)
    seconds = milliseconds / 1000.0
    tp += milliseconds

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                run = not run

        if event.type == KEYUP:
            if event.key == K_q:
                run = False
                board.update_frame()
                board.update()

        if event.type == MOUSEBUTTONUP:
            for i in range(board_size):
                for g in range(board_size):
                    board.map[i][g].pressed = False
        

    pressed = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    if pressed[K_KP0]:
        board.map[0][0].alive = True
        board.update()
        
    if pressed[K_KP2]:
        mat = []
        for i in range(board_size):
            aux = []
            for j in range(board_size):
                if(board.map[i][j].alive == False):
                    aux.append(0)
                else:
                    aux.append(1)
            mat.append(aux)
        
    if pressed[K_r]:
        board.map = []
        board.fill(False)
        board.draw()
    
    if pressed[K_a]:
        board.map = []
        board.fill(True)
        board.draw()

    if run == True and tp >= 1000/speed :
        tp = 0
        board.update_frame()
        board.update()

    if mouse[0]: # makes cells alive
        rects = cell_list()
        for i in range(board_size):
            for g in range(board_size):
                if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+square_size and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+square_size and board.map[i][g].pressed == False:
                    board.map[i][g].alive = True
                    board.map[i][g].pressed = True
                    board.update()

    if mouse[2]: # kills cells
        rects = cell_list()
        for i in range(board_size):
            for g in range(board_size):
                if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+square_size and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+square_size and board.map[i][g].pressed == False:
                    board.map[i][g].alive = False
                    board.map[i][g].pressed = False
                    board.update()

    pygame.display.flip()
