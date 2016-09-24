# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from BiOuterTotalisticCode import BiOuterTotalisticCode
from numpy import zeros
from PIL import Image
import os
from MyImages2Gif import writeGif

class AutomataBiImage(object):

    def __init__(self, mat, size, it, ca, name, dir):
        self.__mat =  mat
        self.__size = len(mat[0])*10
        self.__it = it
        self.__ca = ca
        self.__name = name
        self.__dir = dir
        self.im = []
        self.__image = Image.new("L", (self.size, self.size), "white")       
        self.buildingAutomata(self.ca)
    
    def __startArray(self):
        self.__array = zeros((self.size, self.size))
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                self.__array[i+3][j+3]=self.mat[i][j]
        self.setImage(self.__array, self.name+'xxx', self.dir)
        print(self.__array)
    
    def __putFirstLine(self):
        
        mid = int (self.size/2)
        self.__array[mid][mid] = 1
        
    def tryGetBit(self, i, j):            
        try:
            if ((i<0)or(j<0)):
                return 0
            else:
                return int(self.__array[i][j])
        except IndexError:
            return 0
        
    def getBits(self, line, column):
        
        if (self.ca.neighborhood==5):
            
            b1 = int(self.tryGetBit(line, column))
            b2 = int(self.tryGetBit(line, column+1))
            b3 = int(self.tryGetBit(line+1, column))
            b4 = int(self.tryGetBit(line, column-1))
            b5 = int(self.tryGetBit(line-1, column))
            
            return  self.ca.getNextFive(b1, b2, b3, b4, b5)
        else:
            
            b1 = int(self.tryGetBit(line, column))
            b2 = int(self.tryGetBit(line-1, column-1))
            b3 = int(self.tryGetBit(line-1, column))
            b4 = int(self.tryGetBit(line-1, column+1))
            b5 = int(self.tryGetBit(line, column+1))
            b6 = int(self.tryGetBit(line+1, column+1))
            b7 = int(self.tryGetBit(line+1, column))
            b8 = int(self.tryGetBit(line+1, column-1))
            b9 = int(self.tryGetBit(line, column-1))
            
            return  self.ca.getNextNine(b1, b2, b3, b4, b5 ,b6, b7, b8, b9)
        
    def buildingAutomata(self, ca):    
        self.__startArray()
        bca = zeros((self.size, self.size))
        for k in range(self.it):
            for i in range(self.size):
                for j in range(self.size):
                    bca[i][j]=self.getBits(i,j)                    
            self.__array = bca.copy()
            x = self.name[0:len(self.name)-4]+'('+str(k+1)+')'+self.name[len(self.name)-4:len(self.name)] #gif           
            self.setImage(bca, x+'.png', self.dir) #gif
        self.setImage(bca, self.name, self.dir)   
        self.setGif(self.im) #gif
    
    def setImage(self,array,name,dir):
        aux = []
        for line in range (self.size):
            for column in range (self.size):    
                if(array[line][column]==0):
                    self.image.putpixel((column,line),255)  
                else:
                    self.image.putpixel((column,line),0)
        self.image.save(os.path.expanduser(dir+'/'+name),"png")
        image = Image.open(os.path.expanduser(dir+'/'+name)) #gif
        self.im.append(image) #gif
        
    def setGif(self,im):
        import MyImages2Gif
        
        writeGif('494.gif',im, duration=0.1, dither=0)
       
        
    @property
    def mat(self):
        return self.__mat
        
    @property
    def size(self):
        return self.__size
    
    @property
    def it(self):
        return self.__it

    @property
    def ca(self):
        return self.__ca
    
    @property
    def name(self):
        return self.__name
    
    @property
    def dir(self):
        return self.__dir
    
    @property
    def array(self):
        return self.__array
    
    @property
    def image(self):
        return self.__image

if __name__ == "__main__":
    arq = open('/home/projeto/Música/Arquivos/30P5H2V0 (os).txt','r')
    texto = arq.read()
    arq.close()
    mat = []
    taml = int((len(texto)+1)/(texto.count('\n')+1))
    k = taml
    x = 0
    for i in range (texto.count('\n')):
        linha = []
        for j in range(x,k):
            if(texto[j]=='\n'):
                x = k
                k+=taml
            else:
                if(texto[j]!='\t'):
                    linha.append(int(texto[j]))
        mat.append(linha)
        
    totalistic =  BiOuterTotalisticCode(9,224)
    AutomataBiImage(mat,50,100,totalistic,'30P5H2V0 (os)','/home/projeto/Música/Testes')
    
    
