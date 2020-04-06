import os
import pygame
import random
import settings as s
from sprites import SpriteSheet, Platform, Player, Base, Cloud, Slime, BackGround


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
        self.base_img = pygame.image.load(os.path.join(self.img_dir, 'grassCenter.png')).convert()

        # load background image
        # bg_dir = os.path.join(self.img_dir, 'background')
        # bg_image = pygame.image.load(os.path.join(bg_dir, 'night_city.png')).convert()
        # self.bg_image = pygame.transform.scale(bg_image, (640, 480))

        # load cloud images
        self.cloud_images = []
        cloud_dir = os.path.join(self.img_dir, 'clouds')
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(os.path.join(cloud_dir, f'cloud{i}.png')).convert())

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
        self.clouds = pygame.sprite.Group()

        # load bg image
        self.bg_image = BackGround(self)

        # create new instance of player
        self.player = Player(self)
        self.enemy_timer = 0

        # creating base
        self.bases = []
        base = Base(self, 0)
        self.bases.append(base)
        while base.rect.right < s.WIDTH:
            base = Base(self, base.rect.right)
            self.bases.append(base)

        # creating starting platforms
        for plat in s.PLATFORM_START_LIST:
            Platform(self, *plat)

        # create clouds/other images
        for i in range(5):
            c = Cloud(self)
            c.rect.x -= random.randrange(200, 400, 50)

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
                    if not self.player.jumping:
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

        now = pygame.time.get_ticks()

        # spawn enemy?
        if now - self.enemy_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.enemy_timer = now
            Slime(self)

        # enemy hit?
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_mask)
        if enemy_hits:
            self.playing = False

        # create new bases as player moves
        last_base = self.bases[-1]
        if last_base.rect.right <= s.WIDTH:
            new_base = Base(self, last_base.rect.right, s.HEIGHT - s.BASE_HEIGHT)
            self.bases.append(new_base)
            self.bases.pop(0)

        # player - base collision check
        base_hits = pygame.sprite.spritecollide(self.player, self.bases, False)
        if base_hits:
            lowest = base_hits[0]
            # if player below base, make him rest on base
            if self.player.pos.y > lowest.rect.top:
                self.player.pos.y = lowest.rect.top + 5
                self.player.vel.y = 0
                self.player.jumping = False

        # player - platform collision check
        temp_plat_hits = pygame.sprite.spritecollide(self.player, self.platforms, False)  # BB check
        if temp_plat_hits:  # mask check
            plat_hits = pygame.sprite.spritecollide(self.player, self.platforms, False, pygame.sprite.collide_mask)

        try:
            if plat_hits:
                plat = plat_hits[0]
                for hit in plat_hits:
                    if hit.rect.left > plat.rect.left:
                        plat = hit

                # if player is within the platforms's width
                if self.player.pos.x - self.player.rect.width / 2 < plat.rect.right and \
                        self.player.pos.x + self.player.rect.width / 2 > plat.rect.left:
                    # if player is above platform, make him rest on platform
                    if self.player.pos.y < plat.rect.centery:
                        self.player.pos.y = plat.rect.top + 5  # to compensate for extra space below in image
                        self.player.vel.y = 0
                        self.player.jumping = False
                    # if player is below the platform, and was going/jumping up, restrict his jump
                    if self.player.pos.y > plat.rect.bottom and self.player.vel.y < 0:
                        self.player.pos.y = plat.rect.bottom + self.player.rect.height
                        self.player.vel.y = 0
                        self.player.jumping = False
        except Exception:
            pass

        # moving screen towards right
        if self.player.rect.right >= s.WIDTH * 0.45:
            # creating new clouds
            if random.randrange(100) < s.CLOUD_FREQ:
                Cloud(self)
            if self.player.vel.x > 0:
                # updating player
                self.player.pos.x -= max(self.player.vel.x, 3)
                # updating previous clouds
                for cloud in self.clouds:
                    cloud.rect.x -= max(self.player.vel.x / 4, 3)
                # updating platforms
                for plat in self.platforms:
                    plat.rect.x -= max(self.player.vel.x, 3)
                    if plat.rect.right <= 0:
                        plat.kill()
                        self.score += 1
                # updating enemies
                for enemy in self.enemies:
                    enemy.rect.x -= max(self.player.vel.x, 3)

        # spawn new platforms
        # calculate the right pos of previous platform
        max_right = 0
        for plat in self.platforms:
            if plat.rect.right > max_right:
                max_right = plat.rect.right

        # create new platforms, max of 3 platforms available at a time.
        while len(self.platforms) < 3:
            rand_x = max_right + random.randrange(200, 400)
            rand_y = s.HEIGHT - 150 - s.BASE_HEIGHT - random.randrange(0, 100, 20)
            Platform(self, rand_x, rand_y)

        # player - powerup collision check
        pow_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerUp in pow_hits:
            # play sound

            # add points to score
            self.score += 10

    def draw(self):
        """Draw updated objects to the screen.
        """

        self.screen.fill(s.BLACK)

        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)

        # draw texts
        self.draw_text(f'Score: {self.score}', 22, s.WHITE, s.WIDTH / 2, 15)

        pygame.display.update()

    def show_start_screen(self):
        """Start screen of the game.

        Main menu of the game.
        """

        pygame.mixer.music.load(os.path.join(self.sound_dir, "st.ogg"))
        pygame.mixer.music.play(loops=-1)

        ss_image = pygame.image.load(os.path.join(self.img_dir, 'startscreen.jpeg')).convert()
        ss_image = pygame.transform.scale(ss_image, (640, 480))

        self.screen.blit(ss_image, (0, 0))

        """self.draw_text(s.TITLE, 48, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 1 / 5)
        self.draw_text('Arrows to move and jump, space to shoot.', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 0.5)
        self.draw_text('Press any key to play', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 0.6)"""
        self.draw_text(f'High Score: {self.highscore}', 22, s.WHITE,
                       s.WIDTH / 2, s.HEIGHT * 0.7)

        pygame.display.update()
        self.wait_for_key()

        # fadeout music
        pygame.mixer.music.fadeout(500)

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
