'''
Created on Oct 9, 2016

@author: Nicoli
'''
from PIL import Image
import cv2
import numpy as np
if __name__ == '__main__':
    azul_path = 'data/cell_image/alive_16.png'
    azul = cv2.imread(azul_path)
    azul_list = azul.tolist()
    color_list = []
    for line in azul_list:
        for pixel in line:
            if pixel not in color_list:
                color_list.append(pixel)
    print(color_list)