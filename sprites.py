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


class Platform(pygame.sprite.Sprite):

    def __init__(self, game, x, y, base=False):
        """Initializing a platform sprite.

        Args:
            game (game_instance): Game instance.
            x (int): x coordinate of the center of the platform.
            y (int): y coordinate of the center of the platform.
            base (bool): Whether the platform is used as base ro not.
        """

        self._layer = s.PLATFORM_LAYER
        groups = game.all_sprites, game.platforms
        super(Platform, self).__init__(groups)

        self.game = game

        if base:  # load base image
            self.image = self.game.base_img

        else:  # load a random image
            images = [
                self.game.plat_spritesheet.get_image(0, 96, 380, 94),  # stone
                self.game.plat_spritesheet.get_image(0, 192, 380, 94),  # stone broken
                self.game.plat_spritesheet.get_image(382, 408, 200, 100),  # stone small
                self.game.plat_spritesheet.get_image(232, 1288, 200, 100),  # stone small broken
            ]

            self.image = random.choice(images)

        self.image.set_colorkey(s.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
