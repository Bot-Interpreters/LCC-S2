import os

# game options/settings
TITLE = 'Corona Breakout'
WIDTH = 640
HEIGHT = 480
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'

# game properties
BASE_HEIGHT = 35
POWERUP_SPAWN_FREQ = 80
CLOUD_FREQ = 1
BULLET_SHOOT_FREQ = 1000
VAC_COLLECT = 10
ENEMY_KILLS = 20
PLAT_CROSS = WIDTH / 10
GAME_LEVELS = 4

# player properties
PLAYER_ACC = 0.6
PLAYER_FRICTION = 0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP_VEL = 20
PLAYER_RUN_FREQ = 60
PLAYER_IDLE_FREQ = 100
JUMP_THRESHOLD = 3
BULLET_VEL = 7

# starting platforms
PLATFORM_START_LIST = [
    (WIDTH / 2, HEIGHT / 2),
    (WIDTH * 0.75, HEIGHT * 0.25)
]

# sprite layers
CLOUD_LAYER = 0
BG_IMAGE_LAYER = 1
PLATFORM_LAYER = 2
POW_LAYER = 2
PLAYER_LAYER = 3
ENEMY_LAYER = 3
BULLET_LAYER = 3

# spritesheets
ENEMY_SPRITESHEET = os.path.join('enemy', 'enemies_spritesheet.png')
BAC_SPRITESHEET = os.path.join('enemy', 'bacteria_spritesheet.png')
HUD_SPRITESHEET = os.path.join('hud', 'hud_spritesheet.png')
EXPL_SPRITESHEET = os.path.join('explosions', 'explosions_spritesheet.png')
PLAT_SPRITESHEET = os.path.join('platforms', 'platforms_spritesheet.png')

# player images
PLAYER_IDLE = os.path.join('player', 'Idle')
PLAYER_JUMP = os.path.join('player', 'Jump')
PLAYER_RUN = os.path.join('player', 'Run')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
