
import pygame as pg
import settings
import tilemap
import random
vec = pg.math.Vector2   #transformando o player em um vetor


def colisao_paredes(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, tilemap.collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, tilemap.collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def colisao_paredes2(sprite, group, dir):
     if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.x > 0: #se ele tiver indo pra direita
                sprite.pos.x = hits[0].rect.left - sprite.rect.width #posx = parte esquerda do que ele acertou - width do sprite
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
     if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img    #aplica imagem do player
        self.image = pg.transform.scale(self.image, (64, 112)) #o personagem eh da escala 4x7, entao so podemos fazer multiplos desses para n distorcer a imagem
        self.image_right = game.player_img
        self.image_left = pg.transform.flip(game.player_img, True, False)
        self.image_right = pg.transform.scale(self.image_right, (64,112))
        self.image_left = pg.transform.scale(self.image_left, (64,112))
        self.rect = self.image_right.get_rect()
        self.rect = self.image_left.get_rect()
        self.hit_rect = settings.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center= (x,y)
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.health = settings.PLAYER_HEALTH

    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -settings.PLAYER_SPEED
            self.image = self.image_left
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = settings.PLAYER_SPEED
            self.image = self.image_right
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -settings.PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = settings.PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071


    def update(self):
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        colisao_paredes(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        colisao_paredes(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Ninja(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ninjas
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.ninja_img
        self.image_right = game.ninja_img
        self.image_left = pg.transform.flip(game.ninja_img, True, False)
        self.rect = self.image.get_rect()
        self.rect = self.image_right.get_rect()
        self.rect = self.image_left.get_rect()
        self.hit_rect = settings.NINJA_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center= (x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(x,y)
        self.rot = 0
        self.speed = random.choice(settings.NINJA_SPEED)
        self.target = game.player

    def avoid_mobs(self):
        for ninja in self.game.ninjas:
            if ninja != self:
                dist = self.pos - ninja.pos
                if 0 < dist.length() <settings.AVOID_RADIUS:
                    self.acc += dist.normalize()
    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < settings.DETECT_RADIUS**2:
            #código pra fazer o mob estar sempre olhando pro player
            self.rot = target_dist.angle_to(vec(1, 0))
            if self.rot<180 and self.rot>90:
                self.image = self.image_left
            elif self.rot>(-180) and self.rot<(-90):
                self.image = self.image_left
            else:
                self.image = self.image_right
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1,0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc *self.game.dt **2
    #        self.hit_rect.centerx = self.pos.x
            self.rect.x = self.pos.x
            colisao_paredes2(self, self.game.walls, 'x')    #        self.hit_rect.centery = self.pos.y
            self.rect.y = self.pos.y
            colisao_paredes2(self, self.game.walls, 'y')
    #        print (self.rect.y)
    #        self.rect.center = self.hit_rect.center


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

class Obstacle(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


#       	DESAGIL - PROVA PRATICA
# Na questão de coesão, a classe a seguinte poderia ser melhorada. Ela abrange todos os itens do jogo que não são nem o player nem os mobs,
# e com isso acaba por perder um pouco da coesão, vendo que diferentes itens possuem atributos diferentes e funções diferentes.
# Na função collide já é possível ver isso em como o baú e os outros itens funcionam. Enquanto o baú, quando interagido com, deve abrir e mudar de sprite,
# os outros itens, quando interagidos com, devem ser adicionados ao inventário. E mesmo entre esses itens, suas funções variam. Uma chave, por exemplo,
# deve sumir do inventário quando usada, enquanto uma arma ou uma armadura permanece e é utilizada para aumentar o poder do player. Para melhorar a coesão,
# uma ideia seria criar classes diferentes para os diferentes tipos de itens, como uma classe Keys, uma classe Armor e outra Weapon. Assim, cada classe possui
# uma função específica e bem definida.



class Item (pg.sprite.Sprite):
    def __init__(self,game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos




    def collide(self): #colidir com itens do jogo
        if self.type in ['chest']:
            blocks_hit_list = pg.sprite.spritecollide(Player, self.image, False)
            for block in blocks_hit_list:
                self.image = self.game.items_img[settings.ITEM_IMAGES['bau aberto']]
        if self.type in ['armor'] or self.type in ['weapon'] or self.type in ['key']: #adicionar possíveis itens no inventário
            blocks_hit_list = pg.sprite.spritecollide(Player, self.image, False)
            if pg.KEYDOWN == pg.K_SPACE:
                if self.type in ['armor']:
                    settings.INVENTORY['armor'] = settings.ITEMS_MAP['armor']
                if self.type in ['weapon']:
                    settings.INVENTORY['weapon'] = settings.ITEMS_MAP['weapon']
                if self.type in ['key']:
                    settings.INVENTORY['key'] = settings.ITEMS_MAP['key']
