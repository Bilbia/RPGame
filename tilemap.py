
import pygame as pg
import settings
import pytmx as ptx
#import main
#import os
#from os import path
#import sys


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())       
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * settings.TILESIZE
        self.height = self.tileheight * settings.TILESIZE
        
        
class TiledMap:
    def __init__(self, filename):
        tm = ptx.load_pygame(filename, pixelalpha=True)
#        self.mapw = tm.width
#        self.maph = tm.height
#        tm.tilewidth = tm.tilewidth*4
#        tm.tileheight = tm.tileheight
        self.width = tm.width *tm.tilewidth
        self.height = tm.height *tm.tileheight
        self.tmxdata = tm
        
        
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, ptx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
                        
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
#        temp_surface = pg.transform.scale2x(temp_surface)
        self.render(temp_surface)
        temp_surface = pg.transform.scale2x(pg.transform.scale2x(temp_surface))
#        temp_surface = pg.transform.scale(temp_surface,(self.width,self.height))
        
        return temp_surface




class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height    
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(settings.WIDTH/2)
        y = -target.rect.y + int(settings.HEIGHT/2)
        
        x = min(0, x)
        y = min(0, y)
#        x = max( -settings.WIDTH, x)
#        y = max(-settings.HEIGHT, y)
#        x = max(-(self.width - settings.WIDTH), x)
#        y = max(-(self.height - settings.HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
                        