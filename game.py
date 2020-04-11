import os
import sys
import pygame
import random
import settings as s
from sprites import SpriteSheet, Platform, Player, Base, Cloud, Slime, BackGround, Bullet, Bat


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
        self.paused = False
        self.running = True
        self.load_data()

    def load_data(self):
        """Loads all necessary data.

        Highscore, spritesheets, images, sounds.
        """

        self.dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.dir, 'images')
        self.sound_dir = os.path.join(self.dir, 'sounds')
        self.comic_dir = os.path.join(self.dir, 'Comic Strips')

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
        self.bac_spritesheet = SpriteSheet(os.path.join(self.img_dir, s.BAC_SPRITESHEET))

        # load base image
        self.base_img = pygame.image.load(os.path.join(self.img_dir, 'grassCenter.png')).convert()

        # load virus image
        virus_image = pygame.image.load(os.path.join(self.img_dir, 'coronavirus.png')).convert()
        rect = virus_image.get_rect()
        self.virus_image = pygame.transform.scale(virus_image, (rect.width * 2, rect.height * 2))
        self.virus_image.set_colorkey(s.BLACK)

        # load pause screen image
        image = pygame.image.load(os.path.join(self.img_dir, 'pausescreen.jpg')).convert()
        self.pause_image = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))

        # load mission screen image
        image = pygame.image.load(os.path.join(self.img_dir, 'mis_screen.jpg')).convert()
        self.mis_image = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))

        # load mission failed image
        image = pygame.image.load(os.path.join(self.img_dir, 'mis_failed.jpg')).convert()
        self.mis_failed_image = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))

        # load mission completed image
        image = pygame.image.load(os.path.join(self.img_dir, 'mis_success.jpg')).convert()
        self.mis_completed_img = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))

        # load cloud images
        self.cloud_images = []
        cloud_dir = os.path.join(self.img_dir, 'clouds')
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(os.path.join(cloud_dir, f'cloud{i}.png')).convert())

        # load comic strips
        self.comic_strips = []
        for i in range(1, 17):
            image = pygame.image.load(os.path.join(self.comic_dir, f'scene_{i}.png')).convert()
            image = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))
            self.comic_strips.append(image)

        # load sounds
        self.jump_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, 'jump.wav'))
        self.powerup_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, 'powerup.wav'))
        self.dead_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, 'dead.wav'))
        self.bullet_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, 'bullet.wav'))

    def new(self):
        """Start a new game.
        """

        # keeping track of missions
        self.score = 0
        self.vaccines_collected = 0
        self.enemies_killed = 0
        self.n_bullets = 10  # initial number of bullets for the player

        self.failed = False

        # used for checking if player completed game
        self.platforms_crossed = 0

        # initialize sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.viruses = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()

        # load bg image
        self.bg_image = BackGround(self)

        if self.level > 1:  # needed for scrolling background
            self.bg_image_2 = BackGround(self)
            self.bg_image_2.rect.left = self.bg_image.rect.right

        # create new instance of player
        self.player = Player(self)

        # timer for spawning enemies
        self.slime_timer = 0
        self.bat_timer = 0

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
        if self.level == 1:
            for i in range(5):
                c = Cloud(self)
                c.rect.x -= random.randrange(200, 400, 50)

        # load music
        pygame.mixer.music.load(os.path.join(self.sound_dir, "background.ogg"))

        self.run()

    def run(self):
        """Main Game Loop.

        Event loop begins. Checks for events, updates attributes,
        and finally draws updated objects to the screen.
        """

        # play loaded background music
        pygame.mixer.music.play(loops=-1)

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
                pygame.quit()
                sys.exit(0)

            # escape key to pause
            if event.type == pygame.KEYDOWN:
                # keydown space to jump
                if event.key == pygame.K_UP:
                    if not self.player.jumping:
                        self.player.jump()

                # purely for debugging purposes
                if event.key == pygame.K_F1:
                    self.vaccines_collected += 20
                    self.enemies_killed += 20
                    self.platforms_crossed = s.PLAT_CROSS - 1

                # player shooting
                if event.key == pygame.K_SPACE:
                    # only if not already shooting
                    # prevents spawn of multiple bullets at the same press
                    if not self.player.shooting and self.n_bullets > 0:
                        self.player.shooting = True
                        self.player.idle = False
                        self.bullet_sound.play()
                        Bullet(self)
                        self.n_bullets -= 1

            if event.type == pygame.KEYUP:
                # keyup space to jump_cut
                if event.key == pygame.K_UP:
                    self.player.jump_cut()

                if event.key == pygame.K_SPACE:
                    # if user releases space, set shooting to False
                    self.player.shooting = False

                # pause
                if event.key == pygame.K_ESCAPE:
                    if not self.paused:
                        self.paused = True
                        self.show_pause_screen()

    def update(self):
        """Updates attributes of objects.

        Main logic of the game.
        """

        # update all sprites
        self.all_sprites.update()

        now = pygame.time.get_ticks()

        # spawn Slime at level 1, 2, and 3 every 5 secs.
        if now - self.slime_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            if not self.paused:
                self.slime_timer = now
                Slime(self, self.level >= 3)

        # spawn bat at level 2 and above every 30 secs.
        if self.level == 2:
            bat_freq = 30000
        elif self.level >= 3:
            bat_freq = 10000

        # spawn bats only after level 1
        if self.level > 1:
            if now - self.bat_timer > bat_freq + random.choice([-1000, -500, 0, 500, 1000]):
                if not self.paused:
                    self.bat_timer = now
                    Bat(self, self.level == 4)

        # create new bases as player moves
        last_base = self.bases[-1]
        if last_base.rect.right <= s.WIDTH:
            new_base = Base(self, last_base.rect.right, s.HEIGHT - s.BASE_HEIGHT)
            self.bases.append(new_base)
            self.bases.pop(0)

        # player - enemy collision check
        temp_enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if temp_enemy_hits:
            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_mask)

        try:
            if enemy_hits:
                self.dead_sound.play()
                # reduce player lives
                self.player.lives -= 1
                # is player dead?
                if self.player.lives == 0:
                    self.failed = True
                    self.show_failed_screen()
        except Exception:
            pass

        # player - virus collision check
        temp_virus_hits = pygame.sprite.spritecollide(self.player, self.viruses, False)
        if temp_virus_hits:
            virus_hits = pygame.sprite.spritecollide(self.player, self.viruses, True, pygame.sprite.collide_mask)

        try:
            if virus_hits:
                self.dead_sound.play()
                self.failed = True
                self.show_failed_screen()
        except Exception:
            pass

        # bullet - enemy collision check
        be_hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if be_hits:
            self.dead_sound.play()
            self.score += 20
            self.enemies_killed += 1

        # bullet - platform collision check, if so, bullet sprite will be killed
        pygame.sprite.groupcollide(self.bullets, self.platforms, True, False)

        # player - base collision check
        base_hits = pygame.sprite.spritecollide(self.player, self.bases, False)
        if base_hits:
            lowest = base_hits[0]
            # if player below base, make him rest on base
            if self.player.pos.y > lowest.rect.top:
                self.player.pos.y = lowest.rect.top + 5
                self.player.vel.y = 0
                self.player.jumping = False

        # player - powerup collision check
        pow_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerUp in pow_hits:
            self.powerup_sound.play()
            # add points to score
            self.score += 10
            if powerUp.type == 'vaccine':
                self.vaccines_collected += 1
            elif powerUp.type == 'health':
                self.player.lives += 1
            elif powerUp.type == 'ammo':
                self.n_bullets += 1

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
            if self.level == 1:
                if random.randrange(100) < s.CLOUD_FREQ:
                    Cloud(self)
            if self.player.vel.x > 0:
                # updating player
                self.player.pos.x -= max(self.player.vel.x, 3)
                # updating previous clouds
                for cloud in self.clouds:
                    cloud.rect.x -= max(self.player.vel.x / 6, 1)
                # updating platforms
                for plat in self.platforms:
                    plat.rect.x -= max(self.player.vel.x, 3)
                    if plat.rect.right <= 0:
                        plat.kill()
                        self.score += 1
                        self.platforms_crossed += 1
                # updating enemies
                for enemy in self.enemies:
                    enemy.rect.x -= max(self.player.vel.x, 3)
                # updating viruses
                for virus in self.viruses:
                    virus.rect.x -= max(self.player.vel.x, 3)
                # background
                if self.level >= 2:
                    self.bg_image.rect.x -= max(self.player.vel.x / 6, 1)

        # scrolling background
        if self.level >= 2:
            self.bg_image_2.rect.left = self.bg_image.rect.right
            if self.bg_image.rect.right < 0:
                self.bg_image.rect.left = 0

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

        # check if gameover
        if self.platforms_crossed >= s.PLAT_CROSS:
            if self.enemies_killed >= s.ENEMY_KILLS and self.vaccines_collected >= s.VAC_COLLECT:
                self.playing = False
            else:
                self.failed = True
                self.show_failed_screen()

    def draw(self):
        """Draw updated objects to the screen.
        """

        self.screen.fill(s.BLACK)

        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        self.viruses.draw(self.screen)

        # draw progress bar
        self.draw_text('Level Progress', 15, s.BLACK, 5, s.HEIGHT - s.BASE_HEIGHT, pos='top-left')
        pygame.draw.rect(self.screen, s.RED, (0, s.HEIGHT - 10, s.WIDTH, 10))
        pygame.draw.rect(self.screen, s.GREEN, (0, s.HEIGHT - 10, self.platforms_crossed * 10, 10))

        # draw game info
        self.draw_text(f'Level: {self.level}', 22, s.WHITE, s.WIDTH / 2, 20)

        self.draw_text(f'Player lives remaining: {self.player.lives}', 22, s.RED, 5, 15, pos='top-left')

        self.draw_text(f'Score: {self.score}', 22, s.GREEN, 10, 20, pos='top-right')
        self.draw_text(f'Bullets: {self.n_bullets}', 22, s.GREEN, 10, 40, pos='top-right')

        # dynamically update color for texts
        if self.vaccines_collected < s.VAC_COLLECT:
            vac_color = s.RED
        else:
            vac_color = s.GREEN

        if self.enemies_killed < s.ENEMY_KILLS:
            enem_color = s.RED
        else:
            enem_color = s.GREEN

        self.draw_text(f'Total Vaccines collected: {self.vaccines_collected} / {s.VAC_COLLECT}', 22, vac_color, 5, 45, pos='top-left')
        self.draw_text(f'Total enemies killed: {self.enemies_killed} / {s.ENEMY_KILLS}', 22, enem_color, 5, 75, pos='top-left')

        pygame.display.update()

    def show_start_screen(self):
        """Start screen of the game.

        Main menu of the game.
        """

        pygame.mixer.music.load(os.path.join(self.sound_dir, "start_screen.ogg"))
        pygame.mixer.music.play(loops=-1)

        ss_image = pygame.image.load(os.path.join(self.img_dir, 'startscreen.jpg')).convert()
        ss_image = pygame.transform.scale(ss_image, (s.WIDTH, s.HEIGHT))

        self.screen.blit(ss_image, (0, 0))

        self.draw_text(f'HIGH SCORE: {self.highscore}', 22, s.WHITE,
                       s.WIDTH * 0.5, s.HEIGHT * 0.8)

        pygame.display.update()
        self.wait_for_key(pygame.K_RETURN)

    def show_gameover_screen(self):
        """Game over screen.

        Renders user's score and highscore.
        """

        # load music
        pygame.mixer.music.load(os.path.join(self.sound_dir, "game_over.ogg"))
        pygame.mixer.music.play(loops=-1)

        go_image = pygame.image.load(os.path.join(self.img_dir, 'gameover.jpg')).convert()
        go_image = pygame.transform.scale(go_image, (s.WIDTH, s.HEIGHT))

        self.screen.blit(go_image, (0, 0))

        self.draw_text(f'SCORE: {self.score}', 22, s.RED, s.WIDTH / 2, s.HEIGHT * 0.8)

        if self.score > self.highscore:
            self.highscore = self.score
            # save highscore in local file
            with open(os.path.join(self.dir, s.HS_FILE), 'w') as f:
                f.write(str(self.score))

            self.draw_text('NEW HIGH SCORE!', 22, s.RED, s.WIDTH / 2, s.HEIGHT * 0.9)

        pygame.display.update()
        self.wait_for_key(pygame.K_RETURN)

        # fadeout music
        pygame.mixer.music.fadeout(500)

    def show_pause_screen(self):
        """Pause screen.
        """

        self.screen.blit(self.pause_image, (0, 0))
        self.draw_text(str(self.score), 33, s.WHITE, s.WIDTH * 0.63, s.HEIGHT * 0.395)

        pygame.display.update()
        # if escape key is pressed, game resumes
        self.wait_for_key(pygame.K_ESCAPE)
        self.paused = False

    def show_mission_screen(self):
        """Mission screen.

        Shows the aim and main mission of the game.
        """

        self.screen.blit(self.mis_image, (0, 0))

        self.draw_text(f'Collect at least {s.VAC_COLLECT} vaccines.', 30, s.WHITE, s.WIDTH * 0.5, s.HEIGHT * 0.4)
        self.draw_text(f'Kill a minimum of {s.ENEMY_KILLS} enemies.', 30, s.WHITE, s.WIDTH * 0.5, s.HEIGHT * 0.5)

        pygame.display.update()
        self.wait_for_key(pygame.K_RETURN)

        # fadeout music
        pygame.mixer.music.fadeout(500)

    def wait_for_key(self, key=None):
        """Wait for a key press.

        Args:
            key (pygame.event.key, optional): Key to press to end waiting.
                Defaults to None.
        """

        waiting = True
        pressed = False
        while waiting:
            self.clock.tick(s.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    pressed = True

                if event.type == pygame.KEYUP and pressed:
                    if key is None:
                        waiting = False
                    elif event.key == key:
                        waiting = False

                    # to exit the game loop completely
                    elif event.key == pygame.K_q and pressed:
                        waiting = False
                        self.playing = False
                        self.running = False
                        pygame.quit()
                        sys.exit(0)

    def draw_text(self, text, size, color, x, y, pos='center'):
        """Draws text to screen.

        Args:
            text (str): Text to be displayed.
            size (int): Size of the text.
            color (tuple): Color of the text.
            x (int): x coordinate of the text.
            y (int): y coordinate of the text.
            pos (str): Position of the text, for alignment. Defaults to center.
                Can be of either 'center', 'top-left', 'top-right'
        """

        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)  # antialiasing
        text_rect = text_surface.get_rect()

        if pos == 'center':
            text_rect.centerx = x
            text_rect.centery = y

        elif pos == 'top-left':
            text_rect.left = x
            text_rect.top = y

        elif pos == 'top-right':
            text_rect.top = y
            text_rect.right = s.WIDTH - x

        self.screen.blit(text_surface, text_rect)

    def show_intro_scene(self):
        """Renders a comic strip storyboard.

        Lets the user know the basic plot of the game.
        """

        for image in self.comic_strips[:7]:

            self.screen.blit(image, (0, 0))

            pygame.display.update()
            self.wait_for_key(pygame.K_RETURN)

    def show_completed_screen(self):
        """Renders the last scenes of the game.

        Only if player finishes all missions.
        """

        for image in self.comic_strips[13:]:

            self.screen.blit(image, (0, 0))

            pygame.display.update()
            self.wait_for_key(pygame.K_RETURN)

        self.screen.blit(self.mis_completed_img, (0, 0))

        pygame.display.update()
        self.wait_for_key(pygame.K_RETURN)
        self.playing = False

    def show_failed_screen(self):
        """Renders a mission failed screen.

        If player does not complete missions.
        """

        self.screen.blit(self.mis_failed_image, (0, 0))

        pygame.display.update()
        self.wait_for_key(pygame.K_RETURN)
        self.playing = False

    def show_level_intro(self, level):
        """Renders level info image.

        Args:
            level (int): Level of the game to be played.
        """

        self.level = level

        if self.level == 2:
            for image in self.comic_strips[7:8]:

                self.screen.blit(image, (0, 0))

                pygame.display.update()
                self.wait_for_key(pygame.K_RETURN)

        if self.level == 3:
            for image in self.comic_strips[8:10]:

                self.screen.blit(image, (0, 0))

                pygame.display.update()
                self.wait_for_key(pygame.K_RETURN)

        if self.level == 4:
            for image in self.comic_strips[10:13]:

                self.screen.blit(image, (0, 0))

                pygame.display.update()
                self.wait_for_key(pygame.K_RETURN)

        image = pygame.image.load(os.path.join(self.img_dir, f'level{self.level}.jpg')).convert()
        image = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))

        self.screen.blit(image, (0, 0))

        pygame.display.update()
        self.wait_for_key(pygame.K_RETURN)
