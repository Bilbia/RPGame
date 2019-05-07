# -*- coding: utf-8 -*-
"""
Created on Mon May  6 07:21:05 2019

@author: User
"""
import pygame as pg
import settings

class Player (pg.sprite.Sprite):   
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.image.fill(settings.YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy
        
    def update (self):
        self.rect.x = self.x * settings.TILESIZE
        self.rect.y = self.y * settings.TILESIZE