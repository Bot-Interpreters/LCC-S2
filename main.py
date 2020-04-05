import os
import pygame
import random
import settings as s
from sprites import SpriteSheet, Platform, Player

pygame.mixer.init()  #needed for the background sound

class CoronaBreakout:

    def __init__(self):
        """Initializing attributes for a new game.
        """

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
        pygame.display.set_caption(s.TITLE)

        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(s.FONT_NAME)
        self.running = True
        self.load_data()

    def load_data(self):
        """Loads all necessary data.

        Highscore, spritesheets, images, sounds.
        """

        self.dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.dir, 'images')
        self.sound_dir = os.path.join(self.dir, 'sounds')

        # load high score
        try:  # if file exists, load data
            with open(os.path.join(self.dir, s.HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except Exception:   # else create new file and set highscore to 0
            with open(os.path.join(self.dir, s.HS_FILE), 'w') as f:
                self.highscore = 0

        # load spritesheets
        self.enemy_spritesheet = SpriteSheet(os.path.join(self.img_dir, s.ENEMY_SPRITESHEET))
        self.hud_spritesheet = SpriteSheet(os.path.join(self.img_dir, s.HUD_SPRITESHEET))
        self.expl_spritesheet = SpriteSheet(os.path.join(self.img_dir, s.EXPL_SPRITESHEET))
        self.plat_spritesheet = SpriteSheet(os.path.join(self.img_dir, s.PLAT_SPRITESHEET))

        # load base image
        self.base_img = pygame.image.load(os.path.join(self.img_dir, 'grassCenter.png'))

        # load sounds

    def new(self):
        """Start a new game.
        """

        self.score = 0

        # initialize sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # create new instance of player
        self.player = Player(self)

        # creating base
        self.bases = []
        base = Platform(self, 0, s.HEIGHT - s.BASE_HEIGHT, base=True)
        self.bases.append(base)
        while base.rect.right < s.WIDTH:
            base = Platform(self, base.rect.right, s.HEIGHT - s.BASE_HEIGHT, base=True)
            self.bases.append(base)

        # creating starting platforms
        for plat in s.PLATFORM_LIST:
            Platform(self, *plat)

        # create clouds/other images

        # load music

        self.run()

    def run(self):
        """Main Game Loop.

        Event loop begins. Checks for events, updates attributes,
        and finally draws updated objects to the screen.
        """

        # load music

        self.playing = True

        while self.playing:
            self.clock.tick(s.FPS)
            self.events()
            self.update()
            self.draw()

        # fadeout music

    def events(self):
        """Handling events.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False  # back to start screen
                self.running = False  # closes the whole game

            # escape key to pause

            # keydown space to jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.jump()

            # keyup space to jump_cut
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player.jump_cut()

    def update(self):
        """Updates attributes of objects.

        Main logic of the game.
        """

        # update all sprites
        self.all_sprites.update()

        # base for the player.
        if self.player.pos.y > s.HEIGHT - s.BASE_HEIGHT:
            self.player.pos.y = s.HEIGHT - s.BASE_HEIGHT
            self.player.vel.y = 0

        # create new bases are player moves
        last_base = self.bases[-1]
        if last_base.rect.right <= s.WIDTH:
            new_base = Platform(self, last_base.rect.right, s.HEIGHT - s.BASE_HEIGHT, base=True)
            self.bases.append(new_base)
            self.bases.pop(0)

        # player - platform collision check
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)  # don't kill

        if hits:
            lowest = hits[0]

            # checking x coordinates
            if self.player.pos.x < lowest.rect.right and \
                    self.player.pos.x > lowest.rect.left:
                # checking y coordinates
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False


        '''
        # moving screen towards right
        if self.player.rect.right >= s.WIDTH * 1 / 2:
            if not self.player.jumping:
                self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.y), 2)
                if plat.rect.right <= 0:
                    plat.kill()

        # spawn new platforms
        while len(self.platforms) < 12:
            Platform(self, random.randrange(s.WIDTH - 50, s.WIDTH - 100),
                     random.randrange(s.HEIGHT - 100, s.HEIGHT - 200))
        '''

    def draw(self):
        """Draw updated objects to the screen.
        """

        self.screen.fill(s.BGCOLOR)

        # draw all sprites
        self.all_sprites.draw(self.screen)

        # draw texts

        pygame.display.update()

    def show_start_screen(self):
        """Start screen of the game.

        Main menu of the game.
        """

        # load music
        pygame.mixer.music.load("st.ogg")
        pygame.mixer.music.play()


        self.screen.fill(s.BGCOLOR)

        self.draw_text(s.TITLE, 48, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 1 / 5)
        self.draw_text('Arrows to move and jump, space to shoot.', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 0.5)
        self.draw_text('Press any key to play', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 0.6)
        self.draw_text(f'High Score: {self.highscore}', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 0.7)

        pygame.display.update()
        self.wait_for_key()

        # fadeout music

    def show_gameover_screen(self):
        """Game over screen.

        Renders user's score and highscore.
        """

        if not self.running:
            return None

        # load music

        self.screen.fill(s.BGCOLOR)

        self.draw_text("GAME OVER", 48, s.WHITE, s.WIDTH / 2, s.HEIGHT / 4)
        self.draw_text(f'Score: {self.score}', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT / 2)
        self.draw_text('Press a key to play again', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 3 / 4)

        # draw texts/buttons

        if self.score > self.highscore:
            self.highscore = self.score

            self.draw_text('NEW HIGH SCORE!', 22, s.WHITE,
                           s.WIDTH / 2, s.HEIGHT / 2 + 40)

            with open(os.path.join(self.dir, s.HS_FILE), 'w') as f:
                f.write(str(self.score))

        pygame.display.update()
        self.wait_for_key()

        # fadeout music

    def show_pause_screen(self):
        """Pause screen.
        """

        pass

    def wait_for_key(self):
        """Wait for a key press.
        """

        waiting = True
        while waiting:
            self.clock.tick(s.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        """Draws text to screen.

        Args:
            text (str): Text to be displayed.
            size (int): Size of the text.
            color (tuple): Color of the text.
            x (int): x coordinate of the text.
            y (int): y coordinate of the text.
        """

        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)  # antialiasing
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


if __name__ == '__main__':
    # initializing an instance of the game.
    game = CoronaBreakout()
    game.show_start_screen()

    while game.running:
        game.new()
        game.show_gameover_screen()

    pygame.quit()
