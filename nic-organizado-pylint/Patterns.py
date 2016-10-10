# -*- coding: utf-8 -*-
'''
Created on 3 de out de 2016

@author: pibic-elloa-nicoli
'''
import numpy as np

class Patterns():
    '''Cria as imagens e arquivos dos padrões a ser procurados utilizando arrays
    
        Variáveis da classe:
            - self.start_value: booleano que diz se o estado inicial é branco ou preto
            - self.patterns [nome_do_padrão]: np.array que representa o padrão graficamente
            - self.rotate_dict [nome do padrão]: inteiro que representa quantas vezes este 
            padrão deverá ser rotacionado em 90 graus para ter todos os seus possíveis 
            posicionamentos representados
            - self.patterns_rotated_dict [nome_do_padrão] : lista de np.arrays com os padrões
            rotacionados
            '''
    def __init__(self, start_value):
        '''doc'''
        self.start_value = start_value
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
        self.patterns_rotated_dict = self.rotate_patterns(self.patterns, self.rotate_dict)

    def rotate_patterns(self, patterns_dict, rotated_dict):
        '''Rotaciona os padrões em 90 graus quantas vezes for necessário. 
        Armazena os padrões rotacionados num dicionário de listas, em que cada chave é um padrão que leva a todas as formas que ele pode aparecer
        
        Utiliza:
         '''
        #print(self.patterns)
        for pattern_name in patterns_dict:
            patterns_rotated_dict = {}
            pattern = patterns_dict[pattern_name]
            #print(pattern_name, type(pattern))
            #print(len(pattern))
            #print(pattern)
            num_rot = rotated_dict[pattern_name]
            patterns_rotated_dict[pattern_name] = [np.rot90(pattern, k) for k in range(num_rot)]
            if pattern_name == 'TOAD':
                patterns_rotated_dict[pattern_name].append(np.rot90(pattern.T, 0))
                patterns_rotated_dict[pattern_name].append(np.rot90(pattern.T, 1))
        return pattern_rotated_dict
 
    def patterns_array_to_txt(self, start_value):
        self.rotate_patterns()
        #print(self.patterns_rotated)
        for pattern in self.patterns_rotated_dict:
            for rot in range(len(self.patterns_rotated_dict[pattern])):
                txt_path = self.set_path('txt', start_value, pattern+str(rot))
                np.savetxt(txt_path, self.patterns_rotated_dict[pattern][rot], fmt='%.18g', delimiter=' ', newline='\n')
    
    def set_path(self, mytype, start_value, name):
        if mytype == 'txt':
            extension = '.txt'
        elif mytype == 'img':
            extension = '.png'
        if str(start_value) == 'True':
            path = 'data/patterns/'+ mytype + '/True/' + name + extension
        elif str(start_value) == 'False':
            path = 'data/patterns/' + mytype + '/False/' + name + extension
        return path

    def patterns_array_to_image(self):
        '''doc'''
        self.rotate_patterns()
        for pattern in self.patterns:
            for pos in enumerate(self.patterns[pattern]):
                img_path = self.set_path('imgs', start_value, pattern+str(pos[0]))
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
    def patterns(self):
        '''seta todos os arrays que representam os padrões'''
        self._patterns = {'BLINKER': np.full([3, 5], self.start_value, dtype = np.bool),
                          'BLOCK': np.full([4, 4], self.start_value, dtype = np.bool),
                          'TUB': np.full([5, 5], self.start_value, dtype = np.bool),
                          'BOAT': np.full([5, 5], self.start_value, dtype = np.bool),
                          'GLIDER': np.full([5, 5], self.start_value, dtype = np.bool),
                          'SHIP': np.full([5, 5], self.start_value, dtype = np.bool),
                          'BEEHIVE': np.full([5, 6], self.start_value, dtype = np.bool),
                          'BARGE': np.full([6, 6], self.start_value, dtype = np.bool),
                          'TOAD': np.full([4, 6], self.start_value, dtype = np.bool),
                          'BEACON': np.full([6, 6], self.start_value, dtype = np.bool),
                          'LONG_BOAT': np.full([6, 6], self.start_value, dtype = np.bool),
                          'LOAF': np.full([6, 6], self.start_value, dtype = np.bool),
                          'POND': np.full([6, 6], self.start_value, dtype = np.bool),
                          'MANGO': np.full([6, 7], self.start_value, dtype = np.bool),
                          'LONG_BARGE': np.full([7, 7], self.start_value, dtype = np.bool),
                          'HALF_FLEET': np.full([8, 8], self.start_value, dtype = np.bool),
                          'HALF_BAKERY': np.full([9, 9], self.start_value, dtype = np.bool) }

        self._patterns['BLINKER'][1][1:4] = not self.start_value

        self._patterns['BLOCK'][1][1:3] = not self.start_value
        self._patterns['BLOCK'][2][1:3] = not self.start_value

        self._patterns['TUB'][1][2] = self._patterns['TUB'][2][1] = not self.start_value
        self._patterns['TUB'][2][3] = self._patterns['TUB'][3][2] = not self.start_value

        self._patterns['BOAT'][1][1:3] = self._patterns['BOAT'][3][2] = not self.start_value
        self._patterns['BOAT'][2][1] = self._patterns['BOAT'][2][3] = not self.start_value

        self._patterns['GLIDER'][1][1:4] = not self.start_value
        self._patterns['GLIDER'][2][1] = self._patterns['GLIDER'][3][2] = not self.start_value

        self._patterns['SHIP'][1][1:3] = self._patterns['SHIP'][2][1] = not self.start_value
        self._patterns['SHIP'][3][2:4] = self._patterns['SHIP'][2][3] = not self.start_value

        self._patterns['BEEHIVE'][1][2:4] = self._patterns['BEEHIVE'][2][1] = not self.start_value
        self._patterns['BEEHIVE'][3][2:4] = self._patterns['BEEHIVE'][2][4] = not self.start_value
        
        self._patterns['BARGE'][1][2] = self._patterns['BARGE'][2][1] = not self.start_value
        self._patterns['BARGE'][2][3] = self._patterns['BARGE'][3][2] = not self.start_value
        self._patterns['BARGE'][3][4] = self._patterns['BARGE'][4][3] = not self.start_value

        self._patterns['TOAD'][1][1:4] = self._patterns['TOAD'][2][2:5] = not self.start_value

        self._patterns['BEACON'][1][1:3] = self._patterns['BEACON'][2][1] = not self.start_value
        self._patterns['BEACON'][4][3:5] = self._patterns['BEACON'][3][4] = not self.start_value

        self._patterns['LONG_BOAT'][1][1:3] = self._patterns['LONG_BOAT'][2][1] = not self.start_value
        self._patterns['LONG_BOAT'][2][3] = self._patterns['LONG_BOAT'][3][2] = not self.start_value
        self._patterns['LONG_BOAT'][3][4] = self._patterns['LONG_BOAT'][4][3] = not self.start_value

        self._patterns['LOAF'][1][2:4] = self._patterns['LOAF'][2:4].T[1] = not self.start_value
        self._patterns['LOAF'][2][4] = self._patterns['LOAF'][3][3] = not self.start_value
        self._patterns['LOAF'][4][2] = not self.start_value

        self._patterns['POND'][1][2:4] = self._patterns['POND'][2:4].T[1] = not self.start_value
        self._patterns['POND'][4][2:4] = self._patterns['POND'][2:4].T[4] = not self.start_value

        self._patterns['MANGO'][1][2:4] = self._patterns['MANGO'][4][3:5] = not self.start_value
        self._patterns['MANGO'][2][1] = self._patterns['MANGO'][2][4] = not self.start_value
        self._patterns['MANGO'][3][2] = self._patterns['MANGO'][3][5] = not self.start_value

        self._patterns['LONG_BARGE'][1][2] = self._patterns['LONG_BARGE'][2][1] = not self.start_value
        self._patterns['LONG_BARGE'][2][3] = self._patterns['LONG_BARGE'][3][2] = not self.start_value
        self._patterns['LONG_BARGE'][3][4] = self._patterns['LONG_BARGE'][4][3] = not self.start_value
        self._patterns['LONG_BARGE'][4][5] = self._patterns['LONG_BARGE'][5][4] = not self.start_value

        self._patterns['HALF_FLEET'][1][1:3] = self._patterns['HALF_FLEET'][2][1] = not self.start_value
        self._patterns['HALF_FLEET'][3][2:4] = self._patterns['HALF_FLEET'][2][3] = not self.start_value
        self._patterns['HALF_FLEET'][4][4:6] = self._patterns['HALF_FLEET'][5][4] = not self.start_value
        self._patterns['HALF_FLEET'][6][5:7] = self._patterns['HALF_FLEET'][5][6] = not self.start_value
        #print('HALF FLEET: ',self._patterns['HALF_FLEET'], type(self._patterns['HALF_FLEET']))

        self._patterns['HALF_BAKERY'][1][2:4] = not self.start_value
        self._patterns['HALF_BAKERY'][2][1] = not self.start_value
        self._patterns['HALF_BAKERY'][3][2] = not self.start_value
        self._patterns['HALF_BAKERY'][2:4].T[4] = not self.start_value
        self._patterns['HALF_BAKERY'][4][3] = not self.start_value
        self._patterns['HALF_BAKERY'][4][5:7] = not self.start_value
        self._patterns['HALF_BAKERY'][5][4] = not self.start_value
        self._patterns['HALF_BAKERY'][5:7].T[7] = not self.start_value
        self._patterns['HALF_BAKERY'][6][5] = not self.start_value
        self._patterns['HALF_BAKERY'][7][6] = not self.start_value

