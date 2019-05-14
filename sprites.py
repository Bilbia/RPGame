
import pygame as pg
import settings

class Player(pg.sprite.Sprite):   
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.image.fill(settings.YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0 #Yama
        self.x = x * settings.TILESIZE
        self.y = y * settings.TILESIZE
    
    def get_keys(self): #Yama
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -settings.PLAYER_SPEED     
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = settings.PLAYER_SPEED            
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -settings.PLAYER_SPEED            
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = settings.PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        
    def colisao_paredes(self, dir): #Yama
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
        
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.colisao_paredes('x')
        self.rect.y = self.y
        self.colisao_paredes('y')
        
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        