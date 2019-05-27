import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pg.init()
screenInfo = pg.display.Info() #pega as infos da tela do computador para ajustar o width e o height 

WIDTH = screenInfo.current_w  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = screenInfo.current_h - 28  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = " Teste de movimento "
BGCOLOR = DARKGREY

#ainda a decidir as dimensões, ent vou deixar o que está no tutorial
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Player Settings 

PLAYER_SPEED = 300
PLAYER_IMG = 'raposa pequena.png'   #imagem do player

ITEM_BAU = 'bau'
ITEM_BAU_ABERTO = 'bau_aberto'

ITEM_IMAGES = {
        ITEM_BAU: 'bau.png', #'bau.png',
        ITEM_BAU_ABERTO: 'raposa pequena.png' # 'bau_aberto.png'
}



