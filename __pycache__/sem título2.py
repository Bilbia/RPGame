# -*- coding: utf-8 -*-
"""
Created on Mon May  6 07:21:05 2019

@author: User
"""
import pygame as pg
from settings import *

class Player (pg.sprite.Sprite):   
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_get()
        self.x = x
        self.y = y
        
    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy
        
    def update (self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE