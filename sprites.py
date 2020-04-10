import os
import pygame
import random
import settings as s

vec = pygame.math.Vector2


class SpriteSheet:
    """Utility class for loading and parsing spritesheets.
    """

    def __init__(self, filename):
        """Loads the spritesheet.

        Args:
            filename (str): Filename of the spritesheet to be loaded.
        """

        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height, scale=0.5):
        """Grabs a smaller image from the larger spritesheet.

        Args:
            x (int): x coordinate of the image.
            y (int): y coordinate of the image.
            width (int): width of the image.
            height (int): height of the image.
            scale (float, optional): scale factor between 0 and 1.
                Defaults to 0.5

        Returns:
            image (pygame.Surface): a scaled image.
        """

        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (int(width * scale),
                                               int(height * scale)))

        return image


class Cloud(pygame.sprite.Sprite):

    def __init__(self, game):
        """Initializing a Cloud sprite.

        Args:
            game (game_instance): Game instance.
        """

        self._layer = s.CLOUD_LAYER
        groups = game.all_sprites, game.clouds
        super(Cloud, self).__init__(groups)

        self.game = game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(s.BLACK)
        self.rect = self.image.get_rect()
        scale = random.randrange(50, 101) / 100
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                         int(self.rect.height * scale)))
        self.rect.x = random.randrange(s.WIDTH, s.WIDTH + self.rect.width)
        self.rect.y = random.randrange(0, s.HEIGHT - 350)

    def update(self):
        """Updates sprite.

        Kills the sprite if out of screen.
        """
        if self.rect.right < 0:
            self.kill()


class Platform(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        """Initializing a platform sprite.

        Args:
            game (game_instance): Game instance.
            x (int): x coordinate of the center of the platform.
            y (int): y coordinate of the center of the platform.
        """

        self._layer = s.PLATFORM_LAYER
        groups = game.all_sprites, game.platforms
        super(Platform, self).__init__(groups)

        self.game = game

        # load a random image
        if self.game.level == 1:
            images = [
                self.game.plat_spritesheet.get_image(0, 96, 380, 94),  # stone
                self.game.plat_spritesheet.get_image(0, 192, 380, 94),  # stone broken
                self.game.plat_spritesheet.get_image(382, 408, 200, 100),  # stone small
                self.game.plat_spritesheet.get_image(232, 1288, 200, 100),  # stone small broken
            ]
        else:
            images = [
                self.game.plat_spritesheet.get_image(0, 960, 380, 94),
                self.game.plat_spritesheet.get_image(0, 864, 380, 94),
                self.game.plat_spritesheet.get_image(218, 1558, 200, 100),
                self.game.plat_spritesheet.get_image(382, 0, 200, 100),
            ]

        self.image = random.choice(images)

        self.image.set_colorkey(s.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # spawn a vaccine on the platform
        random_type = random.choice(['vaccine', 'ammo', 'health'])
        if random_type == 'vaccine':
            threshold = 90
        elif random_type == 'ammo':
            threshold = 60
        elif random_type == 'health':
            threshold = 40

        if random.randrange(100) < threshold:
            PowerUp(self.game, self, type_=random_type)


class Base(pygame.sprite.Sprite):

    def __init__(self, game, x):
        """Initializing a Base sprite.

        Args:
            game (game_instance): Game instance.
            x (int): x coordinate of the Base sprite.
        """

        self._layer = s.PLATFORM_LAYER
        groups = game.all_sprites
        super(Base, self).__init__(groups)

        self.game = game
        self.image = self.game.base_img
        self.image.set_colorkey(s.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = s.HEIGHT - s.BASE_HEIGHT


class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        """Initializing player.

        Args:
            game (game_instance): Game instance.
        """

        self._layer = s.PLAYER_LAYER
        groups = game.all_sprites
        super(Player, self).__init__(groups)

        self.game = game
        self.idle = True
        self.running = False
        self.jumping = False
        self.shooting = False
        self.lives = 1

        # tracking for animation
        self.current_frame = 0
        self.last_update = 0

        # load image data
        self.load_images()

        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (20, s.HEIGHT - 50)  # initial pos of player

        self.pos = vec(40, s.HEIGHT - 50)  # position vector
        self.vel = vec(0, 0)  # velocity vector
        self.acc = vec(0, 0)  # acceleration vector

    def load_images(self):
        """Loads all necessary images for animation.
        """

        # standing / idle frames
        self.standing_frames_r = []
        stand_dir = os.path.join(self.game.img_dir, s.PLAYER_IDLE)
        for image in os.listdir(stand_dir):
            frame = pygame.image.load(os.path.join(stand_dir, image)).convert()
            rect = frame.get_rect()
            frame = pygame.transform.scale(frame, (int(rect.width * 0.2),
                                                   int(rect.height * 0.2)))
            frame.set_colorkey(s.BLACK)
            self.standing_frames_r.append(frame)

        self.standing_frames_l = []
        for frame in self.standing_frames_r:  # flip x, and not y
            self.standing_frames_l.append(pygame.transform.flip(frame, True, False))

        # hurt frames
        # self.hurt_frames_r = []
        # hurt_dir = os.path.join(self.game.img_dir, s.PLAYER_HURT)
        # for image in os.listdir(hurt_dir):
        #     frame = pygame.image.load(os.path.join(hurt_dir, image)).convert()
        #     rect = frame.get_rect()
        #     frame = pygame.transform.scale(frame, (int(rect.width * 0.2),
        #                                            int(rect.height * 0.2)))
        #     frame.set_colorkey(s.BLACK)
        #     self.hurt_frames_r.append(frame)

        # self.hurt_frames_l = []
        # for frame in self.hurt_frames_r:  # flip x, and not y
        #     self.hurt_frames_l.append(pygame.transform.flip(frame, True, False))

        # jumping frames
        self.jumping_frames_r = []
        jump_dir = os.path.join(self.game.img_dir, s.PLAYER_JUMP)
        for image in os.listdir(jump_dir):
            frame = pygame.image.load(os.path.join(jump_dir, image)).convert()
            rect = frame.get_rect()
            frame = pygame.transform.scale(frame, (int(rect.width * 0.2),
                                                   int(rect.height * 0.2)))
            frame.set_colorkey(s.BLACK)
            self.jumping_frames_r.append(frame)

        self.jumping_frames_l = []
        for frame in self.jumping_frames_r:  # flip x, and not y
            self.jumping_frames_l.append(pygame.transform.flip(frame, True, False))

        # run frames
        self.run_frames_r = []
        run_dir = os.path.join(self.game.img_dir, s.PLAYER_RUN)
        for image in os.listdir(run_dir):
            frame = pygame.image.load(os.path.join(run_dir, image)).convert()
            rect = frame.get_rect()
            frame = pygame.transform.scale(frame, (int(rect.width * 0.2),
                                                   int(rect.height * 0.2)))
            frame.set_colorkey(s.BLACK)
            self.run_frames_r.append(frame)

        self.run_frames_l = []
        for frame in self.run_frames_r:  # flip x, and not y
            self.run_frames_l.append(pygame.transform.flip(frame, True, False))

        # shooting frames
        self.shooting_frames_r = []
        shot_dir = os.path.join(self.game.img_dir, s.PLAYER_SHOT)
        for image in os.listdir(shot_dir):
            frame = pygame.image.load(os.path.join(shot_dir, image)).convert()
            rect = frame.get_rect()
            frame = pygame.transform.scale(frame, (int(rect.width * 0.2),
                                                   int(rect.height * 0.2)))
            frame.set_colorkey(s.BLACK)
            self.shooting_frames_r.append(frame)

        self.shooting_frames_l = []
        for frame in self.shooting_frames_r:  # flip x, and not y
            self.shooting_frames_l.append(pygame.transform.flip(frame, True, False))

    def jump(self):
        """Jumps the player.

        Jumps only if player is on platform, to avoid double jumping.
        """

        self.rect.x += 2  # see upto 2 pixels below
        plat_hits = pygame.sprite.spritecollide(self, self.game.platforms, False)  # don't kill
        base_hits = pygame.sprite.spritecollide(self, self.game.bases, False)
        self.rect.x -= 2

        hits = plat_hits or base_hits

        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.idle = False
            self.vel.y = s.PLAYER_JUMP_VEL * -1

    def jump_cut(self):
        """Stop the jump if key is released.

        This allows the Player sprite to jump higher iff key is kept
        pressed down.
        """

        if self.jumping:
            if self.vel.y < s.JUMP_THRESHOLD * -1:
                self.vel.y = s.JUMP_THRESHOLD * -1

    def update(self):
        """Update attributes of the player.

        Movements, animation, friction and gravity.
        """

        self.animate()

        # apply gravity to player
        self.acc = vec(0, s.PLAYER_GRAV)

        keys = pygame.key.get_pressed()

        # add acceleration if key is pressed
        if keys[pygame.K_LEFT]:
            self.acc.x = s.PLAYER_ACC * -1
        elif keys[pygame.K_RIGHT]:
            self.acc.x = s.PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * s.PLAYER_FRICTION * -1

        # v = u + at | t = 1
        self.vel += self.acc
        # if vel is very low, stop movement.
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        # x = ut + 0.5 * at**2 | t = 1
        self.pos += self.vel + 0.5 * self.acc

        # prevent player from going towards left
        if self.rect.left < 0:
            self.pos.x = self.rect.left + 50

        # update the position of the sprite with calculated pos
        self.rect.midbottom = self.pos

    def animate(self):
        """Handles player animation.
        """

        now = pygame.time.get_ticks()

        if self.vel.x != 0:
            self.running = True
            self.idle = False
        else:
            self.running = False
            self.idle = True

        # show running animation
        if self.running:
            if now - self.last_update > s.PLAYER_RUN_FREQ:
                self.last_update = now
                # get index of the next frame
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_l)
                bottom = self.rect.bottom

                if self.vel.x > 0:
                    self.image = self.run_frames_r[self.current_frame]
                else:
                    self.image = self.run_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if self.idle:
            if now - self.last_update > s.PLAYER_IDLE_FREQ:
                self.last_update = now
                # get index of the next frame
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_r)
                bottom = self.rect.bottom
                # set image
                self.image = self.standing_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.jumping:
            bottom = self.rect.bottom
            if self.vel.x < 0:
                self.image = self.jumping_frames_l[0]
            else:
                self.image = self.jumping_frames_r[0]

            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # show shooting animation

        self.mask = pygame.mask.from_surface(self.image)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, game):
        """Initialize a bullet sprite.

        Bullets will be fired by the player. Enemy dies if bullet hit.

        Args:
            game (game_instance): Game instance.
        """

        self._layer = s.BULLET_LAYER
        groups = game.all_sprites, game.bullets
        super(Bullet, self).__init__(groups)

        self.game = game
        self.vel = s.BULLET_VEL

        self.load_images()
        self.rect = self.image.get_rect()

        # if player moves towards left while shooting
        if self.game.player.vel.x < 0:
            self.vel *= -1
            self.rect.right = self.game.player.rect.left
        else:
            self.rect.left = self.game.player.rect.right

        self.rect.bottom = self.game.player.rect.centery + 30

    def load_images(self):
        """Loads all necessary images.
        """

        # starting image
        if self.game.level == 4:
            self.image = self.game.expl_spritesheet.get_image(276, 580, 12, 12, scale=1.5)
        else:
            self.image = self.game.expl_spritesheet.get_image(304, 580, 12, 12, scale=1.5)

    def update(self):

        # self.animate()

        # move bullet across screen
        self.rect.x += self.vel

        # if bullet out of screen, kill it
        if self.rect.left > s.WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)


class Slime(pygame.sprite.Sprite):

    def __init__(self, game, bacteria=False):
        """Initialize an enemy sprite.

        Args:
            game (game_instance): Game instance.
            bacteria (bool): Whether to render images of bacteria
        """

        self.layer = s.ENEMY_LAYER
        groups = game.all_sprites, game.enemies
        super(Slime, self).__init__(groups)

        self.game = game
        self.bacteria = bacteria
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.rect.left = s.WIDTH
        self.rect.bottom = s.HEIGHT - s.BASE_HEIGHT + 5
        self.vx = random.randrange(1, 4)  # speed

    def load_images(self):
        """Loads images from spritesheet.
        """

        if not self.bacteria:
            self.walk_images = [
                self.game.enemy_spritesheet.get_image(52, 125, 50, 28, scale=1.5),
                self.game.enemy_spritesheet.get_image(0, 125, 51, 26, scale=1.5)
            ]

        elif self.bacteria:
            self.walk_images = [
                self.game.bac_spritesheet.get_image(0, 0, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(32, 0, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(64, 0, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(0, 31, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(32, 31, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(64, 31, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(0, 62, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(32, 62, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(64, 62, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(0, 93, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(32, 93, 32, 31, scale=1.5),
                self.game.bac_spritesheet.get_image(64, 93, 32, 31, scale=1.5),
            ]

        for frame in self.walk_images:
            frame.set_colorkey(s.BLACK)

    def update(self):
        """Update the sprite.

        Animate, Update position, kill if out of screen.
        """

        self.animate()

        self.rect.x -= self.vx

        if self.rect.right < 0:
            self.kill()

    def animate(self):
        """Handles sprite animation.
        """

        now = pygame.time.get_ticks()

        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.walk_images)
            self.image = self.walk_images[self.current_frame]

        self.mask = pygame.mask.from_surface(self.image)


class Bat(pygame.sprite.Sprite):

    def __init__(self, game, boss=False):
        """Initialize an enemy bat sprite.

        Args:
            game (game_instance): Game instance.
            boss (bool): whether to spawn a boss Bat.
        """

        self.layer = s.ENEMY_LAYER
        groups = game.all_sprites, game.enemies
        super(Bat, self).__init__(groups)

        self.game = game
        self.boss = boss
        self.current_frame = 0
        self.last_update = 0
        self.spreaded = False
        self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = s.WIDTH
        self.rect.top = s.HEIGHT * 0.5
        self.vx = random.randrange(3, 5)
        self.vy = 0
        self.dy = 0.5

    def load_images(self):
        """Loads images from spritesheet.
        """

        if not self.boss:
            self.images = [
                self.game.enemy_spritesheet.get_image(0, 32, 72, 36, scale=1.5),
                self.game.enemy_spritesheet.get_image(0, 0, 75, 31, scale=1.5),
            ]

        elif self.boss:
            self.images = [
                self.game.enemy_spritesheet.get_image(0, 32, 72, 36, scale=2),
                self.game.enemy_spritesheet.get_image(0, 0, 75, 31, scale=2),
            ]

        for image in self.images:
            image.set_colorkey(s.BLACK)

    def update(self):
        """Update the sprite.

        Animate, Update position, kill if out of screen.
        """

        self.animate()

        # moving across screen
        self.rect.x -= self.vx

        # moving up and down
        self.vy += self.dy

        # change direction of y displacement
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1

        # move up or down
        self.rect.y += self.vy

        if self.rect.right < 0:
            self.kill()

        if not self.spreaded and self.rect.centerx < s.WIDTH * 0.9:
            Virus(self.game, self, self.boss)
            self.spreaded = True

    def animate(self):
        """Handles sprite animation.
        """

        now = pygame.time.get_ticks()

        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        self.mask = pygame.mask.from_surface(self.image)


class Virus(pygame.sprite.Sprite):
    """Virus that infects player.

    Player loses one life, plus becomes hurt??
    """

    def __init__(self, game, bat, boss=False):
        """Initializing a virus sprite.

        Spawned by a bat sprite.

        Args:
            game (game_instance): Game Instance.
            bat (Bat): Bat enemy instance.
            boss (bool): Whether to spawn boss virus.
        """

        self.layer = s.ENEMY_LAYER
        groups = game.all_sprites, game.viruses
        super(Virus, self).__init__(groups)

        self.bat = bat
        self.game = game
        self.image = self.game.virus_image
        self.rect = self.image.get_rect()
        if boss:
            self.image = pygame.transform.scale(self.image, (self.rect.width * 2, self.rect.height * 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = self.bat.rect.bottom
        self.rect.centerx = self.bat.rect.centerx
        self.vy = 1
        self.vx = 0
        self.dx = 0.1

    def update(self):
        """Update position of the virus.

        Randomly scatter over the screen.
        """

        # make the virus fall down
        self.rect.y += self.vy

        # move left and right
        self.vx += self.dx

        # change direction of x displacement
        if self.vx > 3 or self.vx < -3:
            self.dx *= -1

        # move left or right
        self.rect.x += self.vx

        if self.rect.bottom > s.HEIGHT - s.BASE_HEIGHT:
            self.vy = 0

        # kill virus if untouched
        if self.rect.right < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """A PowerUp sprite that boosts score.
    """

    def __init__(self, game, plat, type_='vaccine'):
        """Initialize sprite.

        We need a platform sprite to spawn the powerup on.

        Args:
            game (game_instance): Game instance.
            plat (Platform): Platform on which the powerup will spawn.
            type_ (str): Type of powerup to be spawned.
        """

        self._layer = s.POW_LAYER
        groups = game.all_sprites, game.powerups
        super(PowerUp, self).__init__(groups)

        self.game = game
        self.plat = plat
        self.type = type_
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def load_image(self):
        """Loads the image.

        Loads, scaled, rotates.
        """

        if self.type == 'vaccine':
            self.image = pygame.image.load(os.path.join(self.game.img_dir, 'syringe.png')).convert()
            rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (int(rect.width * 2), int(rect.height * 2)))
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.type == 'health':
            self.image = self.game.hud_spritesheet.get_image(0, 94, 53, 45, scale=0.5).convert()
        elif self.type == 'ammo':
            self.image = self.game.plat_spritesheet.get_image(852, 1089, 65, 77, scale=0.5).convert()

        self.image.set_colorkey(s.BLACK)

    def update(self):
        """Update sprite.

        Move, Kill it if not on platform.
        """

        # moving powerup along with platform
        self.rect.centerx = self.plat.rect.centerx

        if not self.game.platforms.has(self.plat):
            self.kill()


class BackGround(pygame.sprite.Sprite):
    """A class for bg images.

    Used only for layering functionality.
    """

    def __init__(self, game):
        """Initializing a new background.

        Args:
            game (game_instance): Game instance.
        """

        self._layer = s.BG_IMAGE_LAYER
        groups = game.all_sprites
        super(BackGround, self).__init__(groups)

        self.game = game

        bg_dir = os.path.join(self.game.img_dir, 'background')

        if self.game.level >= 2:
            image = pygame.image.load(os.path.join(bg_dir, 'forest.jpg')).convert()
        else:
            image = pygame.image.load(os.path.join(bg_dir, 'night_city.png')).convert_alpha()
            image.set_colorkey(s.BLACK)

        self.image = pygame.transform.scale(image, (s.WIDTH, s.HEIGHT))
        self.rect = self.image.get_rect()
