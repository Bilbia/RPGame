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
        if not self.colisao_paredes(dx,dy):
            self.x += dx
            self.y += dy
        
    def colisao_paredes (self, dx = 0, dy = 0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                print("com parede")
                return True
            print("sem parede")
            return False
        
    def update (self):
        self.rect.x = self.x * settings.TILESIZE
        self.rect.y = self.y * settings.TILESIZE
        
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((settings.TILESIZE,settings.TILESIZE))
        self.image.fill(settings.RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE