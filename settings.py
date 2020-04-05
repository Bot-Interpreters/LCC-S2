import os
import settings as s

# game options/settings
TITLE = 'Corona Breakout'
WIDTH = 640
HEIGHT = 480
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'

# game properties
BASE_HEIGHT = 35

# player properties
PLAYER_ACC = 0.6
PLAYER_FRICTION = 0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP_VEL = 20
JUMP_THRESHOLD = 3
PLAYER_RUN_FREQ = 70
PLAYER_IDLE_FREQ = 100

# starting platforms
PLATFORM_LIST = [
    (s.WIDTH / 2, s.HEIGHT / 2),
    (s.WIDTH * 0.75, s.HEIGHT * 0.25)
]

# sprite layers
PLATFORM_LAYER = 1
PLAYER_LAYER = 1

# spritesheets
ENEMY_SPRITESHEET = os.path.join('enemy', 'enemies_spritesheet.png')
HUD_SPRITESHEET = os.path.join('hud', 'hud_spritesheet.png')
EXPL_SPRITESHEET = os.path.join('explosions', 'explosions_spritesheet.png')
PLAT_SPRITESHEET = os.path.join('platforms', 'platforms_spritesheet.png')

# player images
PLAYER_HURT = os.path.join('player', 'Hurt')
PLAYER_IDLE = os.path.join('player', 'Idle')
PLAYER_JUMP = os.path.join('player', 'Jump')
PLAYER_RUN = os.path.join('player', 'Run')
PLAYER_SHOT = os.path.join('player', 'Shot')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
OLIVEGREEN = (186, 184, 108)
GREENYELLOW = (173,255,47)
BGCOLOR = GREENYELLOW 	#sai changed bg colour from light blue to olive green