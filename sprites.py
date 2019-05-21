
import pygame as pg
import settings
vec = pg.math.Vector2   #transformando o player em um vetor

class Player(pg.sprite.Sprite):   
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img    #aplica imagem do player
        self.image = pg.transform.scale(self.image, (64, 112)) #o personagem eh da escala 4x7, entao so podemos fazer multiplos desses para n distorcer a imagem
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * settings.TILESIZE
    
    def get_keys(self): #Yama
        self.vel = vec(0,0)
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -settings.PLAYER_SPEED     
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = settings.PLAYER_SPEED            
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -settings.PLAYER_SPEED            
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = settings.PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        
    def colisao_paredes(self, dir): #Yama
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
        
    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.colisao_paredes('x')
        self.rect.y = self.pos.y
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
        
        
class Item (pg.sprite.Sprite):
    def __init__(self,game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        