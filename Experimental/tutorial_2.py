import pygame

"""
A bit more advanced script
Don't alter code in this file, create a copy and of this file
Put the copy in any other folder, and work on it.
"""


class Block:
    """Creating a class for Block object
    """

    def __init__(self, x, y, height, width, color):
        """Initializing an instance of Block object

        Args:
            x (int): x coordinate of the block's top left corner
            y (int): y coordinate of the block's top left corner
            height (int): height of the block
            width (int): width of the block
            color (tuple): color of the block
        """

        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.vel = 10  # velocity of the block

    def draw_to_surface(self, surface):
        """Drawing the block that we created to a surface

        Args:
            surface (pygame.Surface): a surface to draw the block on
        """

        pygame.draw.rect(surface, self.color, [self.x, self.y, self.width, self.height])


pygame.init()

SCREEN_WIDTH = 416
SCREEN_HEIGHT = 312
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tutorial 2')

# loading a background image into a variable
background = pygame.image.load('background.jpg')

clock = pygame.time.Clock()

block = Block(x=200, y=150, height=10, width=70, color=WHITE)


def update_surface():
    """Updating the surface

    This function can be simply called at the end to the event loop
    to draw all the objects and update the surface.
    """

    # drawing the background
    surface.blit(background, (0, 0))

    # drawing the block on the surface
    block.draw_to_surface(surface)

    # updating the display for every iteration
    pygame.display.update()


run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:
                # reset the position of the block
                block.x = 200
                block.y = 150

    keys = pygame.key.get_pressed()

    """If the block hits the boundary of the surface, we are not going
    to update the position of the block.
    """

    if keys[pygame.K_RIGHT] and block.x + block.width <= SCREEN_WIDTH:
        # checking whether the block hit the left side
        block.x += block.vel

    elif keys[pygame.K_LEFT] and block.x > 0:
        # checking whether the block hit the right side
        block.x -= block.vel

    if keys[pygame.K_UP] and block.y > 0:
        # checking whether the block hit the top side
        block.y -= block.vel

    elif keys[pygame.K_DOWN] and block.y + block.height + 10 <= SCREEN_HEIGHT:
        # checking whether the block hit the botom side
        # + 10 just acts like padding, ignore it.
        block.y += block.vel

    update_surface()

pygame.quit()
