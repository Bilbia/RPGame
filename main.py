
import pygame as pg
import sys
import settings  
import sprites 
import tilemap
import os
from os import path


#Primeiro passo: definir a malha por onde o pernosagem se movimentará
#o que é um "set" --> coleção de itens desordenados, sendo cada um deles único e imutável, n podendo copiá-los

class Game: # o que vai aparecer na tela do jogo
    
    #chuva de funções iniciais
    
    def __init__(self): #--> __init__ : construtor d elementos do jogo
        pg.init()
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT),pg.RESIZABLE) #escolhendo largura e altura da malha quadriculada
        os.environ['SDL_VIDEO_CENTERED'] = '1' #centraliza a janela do jogo na tela do computador
        pg.display.set_caption(settings.TITLE) 
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "Sprites")
        map_folder = path.join(game_folder, "Maps")
        self.map = tilemap.TiledMap(path.join(map_folder, 'entrada.tmx'))
        self.map_img = self.map.make_map()
        self.intro_img = pg.image.load(path.join(img_folder, settings.INTRO_IMG)).convert_alpha()
#        self.map_img = pg.transform.scale(self.map_img,(4*settings.WIDTH,4*settings.HEIGHT))
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, settings.PLAYER_IMG)).convert_alpha()  #imagem do player
        self.item_images = {}
        for item in settings.ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, settings.ITEM_IMAGES[item])).convert_alpha()
        self.ninja_img = pg.image.load(path.join(img_folder, settings.NINJA_IMG)).convert_alpha()
            
        
    def new(self):
            self.all_sprites = pg.sprite.Group() 
            self.walls = pg.sprite.Group()
            self.items = pg.sprite.Group()
            self.ninjas = pg.sprite.Group()
            
            for tile_object in self.map.tmxdata.objects:
                obj_center = settings.vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                if tile_object.name == 'player':
                    self.player = sprites.Player(self, obj_center.x, obj_center.y)
                if tile_object.name == 'wall':
                        sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name == 'ninja':
                    sprites.Ninja(self, obj_center.x, obj_center.y)
                if tile_object.name in ['chest']:
                    sprites.Item(self,obj_center,tile_object.name)
                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name == 'door':
                    sprites.Item(self,obj_center,tile_object.name)
                    self.porta = self.rect = sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
#                    return porta
                if tile_object.name in ['key']:
                    sprites.Item(self,obj_center,tile_object.name)
                    self.key = sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)

                if tile_object.name in ['casaco']:
                    sprites.Item(self,obj_center,tile_object.name)
                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
#                    
#                if tile_object.name in ['guarda_chuva']:
#                    sprites.Item(self,obj_center,tile_object.name)
#                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                    
                
            self.camera = tilemap.Camera(self.map.width, self.map.height)
            self.draw_debug = False
           
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS)/1000
            self.events()
            self.update()
            self.draw()
            
    def quit (self):
        pg.quit()
        sys.exit()
        
    def update(self):
        self.all_sprites.update() #atualizar a cada loop feito
        self.camera.update(self.player)
        keys = pg.key.get_pressed()
        hits = pg.sprite.spritecollide(self.player, self.items, False) #checa colisão do player com o item
        
        #mecanismo de interagir com objetos
        for hit in hits:
            #mecanismo do bau
            if keys[pg.K_SPACE]: #checa se a tecla espaço foi apertada
                if hit.type == 'chest':
                    if 'chest_key' in settings.INVENTORY: #checa se a chave do bau tá no inventário
                        hit.kill() #deleta a sprite do bau
                        for tile_object in self.map.tmxdata.objects:
                            obj_center = settings.vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                            if tile_object.name in ['chest']:
                                sprites.Item(self,obj_center,'bau aberto') #cria a sprite do bau fechado    
                        settings.INVENTORY.append("door_key")  #adiciona chave da porta
                #mecanismo da porta
                if hit.type == 'door':
                    if 'door_key' in settings.INVENTORY: #checa se a chave da porta tá no inventário
                        self.porta.kill()
                        for tile_object in self.map.tmxdata.objects:
                            obj_center = settings.vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                            if tile_object.name in ['door']:
                                sprites.Item(self,obj_center,'porta aberta')
                                
                if hit.type == 'key':
                   hit.kill()
                   self.key.kill()
                   settings.INVENTORY.append('key')
                   
                if hit.type == 'casaco':
                   hit.kill()
                   self.key.kill()
                   settings.INVENTORY.append('casaco')
#                    
#                if hit.type == 'guarda_chuva':
#                    hit.kill()
#                    settings.INVENTORY.append('guarda_chuva')

    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (x, 0), (x, settings.HEIGHT)) # DESENHANDO AS LINHAS HORIZONTAIS
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (0, y), (settings.WIDTH, y))
            
        
    def draw (self):
        # detalhe:  sprites são "imagens" 2d, parte de um gráfico maior, que seria a cena.
#        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(settings.BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
#        self.draw_grid() #GRADEE
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, settings.YELLOW, self.camera.apply_rect(sprite.rect),1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, settings.YELLOW, self.camera.apply_rect(wall.rect),1)
        pg.display.flip()
        
    def events(self):
        #bora colocar eventos here --> ações que o usuário pode fazer
        for event in pg.event.get(): # --> chamar função para sair do jogo
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_I: #aparecer tela com inventário
                    ITEMS_MAP = True
                    while ITEMS_MAP:
                        self.clock.tick(settings.FPS)
                        background_colour = (255,255,255)
                        (width, height) = (300, 200)
                        screen = pg.display.set_mode((width, height))
                        pg.display.set_caption('Tutorial 1')
                        screen.fill(background_colour)
                        pg.display.flip()
                        running = True
                        while running:
                          for event in pg.event.get():
                            if event.type == pg.QUIT:
                              running = False
                        
                        
                if event.key == pg.K_ESCAPE:
                    self.quit()
                
                #arrumar o tamanho da tela
                if event.key == pg.K_f and pg.key.get_mods() & pg.KMOD_ALT:
                    #se apertar ALT + F, a tela fica fullscreen
                    pg.display.quit()
                    pg.display.init()
                    self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                
                elif event.key == pg.K_g and pg.key.get_mods() & pg.KMOD_ALT:
                    #se apertar ALT + G (ia ficar ruim colocar W mas pode ser outra), a tela fica windowed
                    pg.display.quit()
                    pg.display.init()
                    self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT), pg.RESIZABLE)
                    
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
            
        
                
                
    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass
 
    
#objeto do jogo
        
g = Game()
g.show_start_screen()

while True:
#    g.game_intro()
    g.new()
    g.run()
    g.show_go_screen()
        