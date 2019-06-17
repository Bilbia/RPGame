import pygame as pg
import sys
import settings
import sprites
import tilemap
import os
from os import path

#Primeiro passo: definir a malha por onde o pernosagem se movimentará
#o que é um "set" --> coleção de itens desordenados, sendo cada um deles único e imutável, n podendo copiá-los

#HUD functions
#desenha a barra de vida do player
def draw_player_health(surf, x, y, pct):
    if pct<0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct > 0.6:
        col = settings.GREEN
    elif pct >0.3:
        col = settings.YELLOW
    else:
        col = settings.RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, settings.WHITE, outline_rect, 2)

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
        self.background = pg.image.load(path.join(img_folder, 'start.jpg')).convert()
        self.map_img = self.map.make_map()
        self.intro_img = pg.image.load(path.join(img_folder, settings.INTRO_IMG)).convert_alpha()
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

            #define onde sprites vão ser desenhados baseado no mapa tmx
            for tile_object in self.map.tmxdata.objects:
                obj_center = settings.vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                if tile_object.name == 'player':
                    self.player = sprites.Player(self, obj_center.x, obj_center.y) #define spawn point do player
                if tile_object.name == 'wall':
                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height) #cria obstáculo das paredes pra colisão
                if tile_object.name == 'ninja':
                    sprites.Ninja(self, obj_center.x, obj_center.y)
                if tile_object.name in ['chest']:
                    sprites.Item(self,obj_center,tile_object.name)
                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name in ['door']:
                    sprites.Item(self,obj_center,tile_object.name)
                    self.porta = sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name == 'door_final':
                    sprites.Item(self,obj_center,tile_object.name)
                    self.porta2 = sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name in ['key']:
                    sprites.Item(self,obj_center,tile_object.name)
                    self.key = sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name in ['casaco']:
                    sprites.Item(self,obj_center,tile_object.name)
                    self.casaco = sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
#                if tile_object.name in ['guarda_chuva']:
#                    sprites.Item(self,obj_center,tile_object.name)
#                    sprites.Obstacle(self, 4*tile_object.x, 4*tile_object.y, 4*tile_object.width, 4*tile_object.height)
                if tile_object.name == 'book':
                    sprites.Item(self,obj_center,tile_object.name)
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
        keys = pg.key.get_pressed() #checa qual tecla foi pressionada

        hits = pg.sprite.spritecollide(self.player, self.ninjas, False, tilemap.collide_hit_rect)
        for hit in hits:
            self.player.health -= settings.NINJA_DAMAGE
            hit.vel = sprites.vec(0,0)
            if self.player.health <=0:
                self.playing = False
                settings.INVENTORY = []
                settings.PLAYER_SPEED = 300
                settings.PLAYER_HEALTH = 100
        if hits:
            self.player.pos += sprites.vec(settings.NINJA_KNOCKBACK,0).rotate(-hits[0].rot)

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
                        self.porta.kill() #deleta o rect que causa a colisão e permite atravessar
                        for tile_object in self.map.tmxdata.objects:
                            obj_center = settings.vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                            if tile_object.name in ['door']:
                                sprites.Item(self,obj_center,'porta aberta') #coloca a sprite da porta aberta no lugar de onde tava a porta fechada
                if hit.type == 'door_final':
                    self.porta2.kill()
                    for tile_object in self.map.tmxdata.objects:
                            obj_center = settings.vec(4*tile_object.x + 4*tile_object.width/2, 4*tile_object.y + 4*tile_object.height / 2)
                            if tile_object.name in ['door']:
                                sprites.Item(self,obj_center,'porta aberta')
                                self.quit()

                if hit.type == 'key':
                   hit.kill()
                   self.key.kill()
                   settings.INVENTORY.append('chest_key')
                if hit.type == 'casaco':
                   hit.kill()
                   self.casaco.kill()
                   settings.INVENTORY.append('casaco')
                   settings.PLAYER_HEALTH += 40
                   self.player.health += 40
#                if hit.type == 'guarda_chuva':
#                    hit.kill()
#                    settings.INVENTORY.append('guarda_chuva')
                if hit.type == 'book':
                        hit.kill() #deleta o rect de colisão pra n poder pegar o livro mais de uma vez
                        settings.PLAYER_SPEED = settings.PLAYER_SPEED*1.25  #aumenta velocidade do player em 50%


    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (x, 0), (x, settings.HEIGHT)) # DESENHANDO AS LINHAS HORIZONTAIS
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (0, y), (settings.WIDTH, y))


    def draw (self):
        # detalhe:  sprites são "imagens" 2d, parte de um gráfico maior, que seria a cena.
        self.screen.fill(settings.BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, settings.YELLOW, self.camera.apply_rect(sprite.rect),1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, settings.YELLOW, self.camera.apply_rect(wall.rect),1)
        #HUD
        draw_player_health(self.screen, 10, 10, self.player.health/settings.PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        #bora colocar eventos here --> ações que o usuário pode fazer
        for event in pg.event.get(): # --> chamar função para sair do jogo
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:



                if event.key == pg.K_i:
                    Game.inventory()

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

    def text_objects(text,color,size):
        if size == "small":
            textSurface = settings.smallfont.render(text, True, color)
        elif size == "medium":
            textSurface = settings.medfont.render(text, True, color)
        elif size == "large":
            textSurface = settings.largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_to_screen(msg,color, y_displace=0, size = "small"):
        textSurf, textRect = Game.text_objects(msg,color, size)
        textRect.center = (settings.WIDTH2 / 2), (settings.HEIGHT2/ 2)+y_displace
        settings.gameDisplay.blit(textSurf, textRect)


    def inventory():
        invent = True
        while invent:
            for event in pg.event.get(): # --> chamar função para sair do jogo
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key ==pg.K_c:
                        invent = False
                    elif event.key == pg.K_q:
                        pg.quit()
                        quit()
            settings.gameDisplay.fill(settings.BLACK)



            Game.message_to_screen("Inventory",
                                   settings.WHITE,
                                   -200,
                                   size = "medium")

            Game.message_to_screen("press Q to quit or C to continue",
                                   settings.WHITE,
                                   200,
                                   size = "small")

            Game.message_to_screen("{0}".format(settings.INVENTORY),
                                   settings.WHITE,
                                   100,
                                   size = "small")

            pg.display.update()
            settings.clock.tick(5)







    def start_screen(self):
    # Variável para o ajuste de velocidade
        clock = pg.time.Clock()

        # Carrega o fundo da tela inicial

        self.background_rect = self.background.get_rect()

        running = True
        while running:

            # Ajusta a velocidade do jogo.
            clock.tick(settings.FPS)

            # Processa os eventos (mouse, teclado, botão, etc).
            for event in pg.event.get():
#                 Verifica se foi fechado.
                if event.type == pg.K_ESCAPE:
                    state = settings.QUIT

                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = settings.GAME


                        running = False





            # A cada loop, redesenha o fundo e os sprites
            self.screen.fill(settings.BLACK)
            self.screen.blit(self.background, self.background_rect)

            # Depois de desenhar tudo, inverte o display.
            pg.display.flip()




        return state



    def show_go_screen(self):
        pass


g = Game()


while True:
    g.start_screen()
    g.new()
    g.run()
    g.show_go_screen()
