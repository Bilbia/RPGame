# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:26:47 2019

@author: NAmandita
"""

import pygame as pg
import sys
import settings  
import sprites  


#Primeiro passo: definir a malha por onde o pernosagem se movimentará
#o que é um "set" --> coleção de itens desordenados, sendo cada um deles único e imutável, n podendo copiá-los


class Game: # o que vai aparecer na tela do jogo
    
    #chuva de funções iniciais
    
    def __init__(self): #--> __init__ : construtor d elementos do jogo
        pg.init()
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT)) #escolhendo largura e altura da malha quadriculada
        pg.display.set_caption(settings.TITLE) 
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()
        
    def load_data(self):
        pass # ferramenta de fluxo do pragrama, que preenche lacunas e permite que o programa passe. Nesse caso, é adicionado pq a função, para existir, precisa de uma linha após o "def". Com o pass eu garanto que o código use essa função
        
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = sprites.Player(self, 0, 0)
        for x in range(10,20):
            sprites.Wall(self, x, 10)
           
           
       
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def quit (self):
        pg.quit()
        sys.exit()
        
    def update(self):
        self.all_sprites.update() #atualizar a cada loop feito
        
        
        
    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (x,0), (x, settings.HEIGHT)) # DESENHANDO AS LINHAS HORIZONTAIS
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.RED, (0,y), (settings.WIDTH,y))
            
        
    def draw (self):
        # detalhe só pra n esquecer pq sou monga:  sprites são "imagens" 2d, parte de um gráfico maior, que seria a cena.
        self.screen.fill(settings.BGCOLOR)
        self.draw_grid() #GRADEE
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        
    def events(self):
        #bora colocar eventos here --> ações que o usuário pode fazer
        for event in pg.event.get(): # --> chamar função para sair do jogo
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx = -1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx = 1)
                if event.key == pg.K_UP:
                    self.player.move(dy = -1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy = 1)
                
    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass
 
    
#objeto do jogo
        
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()
    g.show_go_screen()
    

        
