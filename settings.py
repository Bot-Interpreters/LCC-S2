import os
import settings as s

# game options/settings
TITLE = 'Corona Breakout'
WIDTH = 640
HEIGHT = 480
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'

# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# starting platforms
PLATFORM_LIST = [
    (s.WIDTH / 2, s.HEIGHT / 2),
    (s.WIDTH * 0.75, s.HEIGHT * 0.25)
]

# sprite layers
PLATFORM_LAYER = 1

# spritesheets
ENEMY_SPRITESHEET = os.path.join('enemy', 'enemies_spritesheet.png')
HUD_SPRITESHEET = os.path.join('hud', 'hud_spritesheet.png')
EXPL_SPRITESHEET = os.path.join('explosions', 'explosions_spritesheet.png')
PLAT_SPRITESHEET = os.path.join('platforms', 'platforms_spritesheet.png')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
