from os import path
import pygame as pg
vec = pg.math.Vector2


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
PLAYER_HIT_RECT = pg.Rect(0,0,64,112)
PLAYER_HEALTH = 100

    
#Intro Image
INTRO_IMG = 'start.jpg'


#Ninja Settings
NINJA_IMG = 'ninja 1.2.png'
NINJA_SPEED = [200,150,175,100,75,125]
NINJA_HIT_RECT = pg.Rect(0,0,64,64)
NINJA_DAMAGE = 10
NINJA_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 1600

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1



#Imagens dos Items
ITEM_IMAGES = {
        'chest': 'chest_close.png', 
        'bau aberto': 'chest_open.png', 
        'door' : 'porta trancada.png',
        'porta aberta': 'porta aberta.png',
        'key': 'chave.png',
        'casaco': 'casaco.png',
#        'guarda_chuva': 'guarda_chuva.png'
        'book': 'invisivel.png',
        'door_final' : 'porta trancada.png'        
}

ITEMS_MAP = {
        'armor': {
                'img': 'casaco.png',
                'defense': 40,
                'description': "quentinho, te protege do frio..."
        },
                
        'weapon': {
                'img': 'prototipo.png',
                'attack': 50,
                'description': "quebrou e não serve para mais nada... Essas pontas de parafuso devem servir para matar alguém"
        },
        
        'key': "Pode servir para desbloquear uma área importante!!"
                
}

INVENTORY = [
        ]


#config. para textos
smallfont = pg.font.SysFont("comicsansms", 25)
medfont = pg.font.SysFont("comicsansms", 50)
largefont = pg.font.SysFont("comicsansms", 80)
WIDTH2 = screenInfo.current_w  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT2 = screenInfo.current_h - 28  # 16 * 48 or 32 * 24 or 64 * 12

clock = pg.time.Clock()

gameDisplay = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Backpack')

GAME = 0
QUIT = 1





