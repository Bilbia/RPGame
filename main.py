5
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
        
        
#        self.items_img = {
#            settings.ITEM_BAU: pg.image.load(path.join(img_folder, settings.ITEM_IMAGES[settings.ITEM_BAU])).convert_alpha(),
#            settings.ITEM_BAU_ABERTO: pg.image.load(path.join(img_folder, settings.ITEM_IMAGES[settings.ITEM_BAU_ABERTO])).convert_alpha()
#        }
        
    def new(self):
            self.all_sprites = pg.sprite.Group() 
            self.walls = pg.sprite.Group()
            self.items = pg.sprite.Group()
    
#            for row, tiles in enumerate(self.map.data):
#                for col, tile in enumerate(tiles):
#                    if tile == '1':
#                        self.walls.add(sprites.Wall(self, col, row))
#                    if tile == 'P':
#                        self.player = sprites.Player(self, col, row)
#                        self.all_sprites.add(self.player)
#                    if tile == 'B':
#                        item = sprites.Item(self,col,row,settings.ITEM_BAU)
#                        self.items.add(item)
#                        self.all_sprites.add(item)
            
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                if tile_object.name == 'player':
                    self.player = sprites.Player(self, 4*tile_object.x, 4*tile_object.y)
                if tile_object.name == 'wall':
                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
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
        
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits: #se o player bater no objeto bau e apertar espaço, abrirá outra imagem com o baí aberto.
#            for event in pg.event.get(): # --> chamar função para sair do jogo
                if hit.type == settings.ITEM_IMAGES['raposa pequena.png'] and hit.type == pg.K_SPACE:
                    'B' == settings.ITEM_IMAGES['raposa pequena.png']               

    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (x, 0), (x, settings.HEIGHT)) # DESENHANDO AS LINHAS HORIZONTAIS
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (0, y), (settings.WIDTH, y))
            
        
    def draw (self):
        # detalhe só pra n esquecer pq sou monga:  sprites são "imagens" 2d, parte de um gráfico maior, que seria a cena.
        #self.screen.fill(settings.BGCOLOR)
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
                        
                    
#    def game_intro(self):
#        self.screen.blit(self.intro_img, tilemap.Camera.apply_rect(self.map_rect))
#        for event in pg.event.get(): # --> chamar função para sair do jogo
#            if event.type == pg.QUIT:
#                self.quit()
#            if event.type == pg.KEYDOWN:
#                if event.key == pg.K_ESCAPE:
#                    self.quit()
#                if event.key == pg.K_SPACE:
#                    pass
            
                
                
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
        