import pygame

"""
This script will introduce the basics of pygame.
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

        """
        making these self.variable will allow us to access these
        variables among other methods(functions under the same class)
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color

        # additional attributes that our block can have
        self.vel = 10  # velocity of the block

    def draw_to_surface(self, surface):
        """Drawing the block that we created to a surface

        Args:
            surface (pygame.Surface): a surface to draw the block on
        """

        pygame.draw.rect(surface, self.color, [self.x, self.y, self.width, self.height])


# initializing pygame
pygame.init()

# setting some constants
SCREEN_WIDTH = 800  # width of the surface
SCREEN_HEIGHT = 600  # height of the surface
FPS = 60  # how many times to refresh the surface per second

# colors - (Red, green, blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# creating a new pygame.Surface to draw our objects on
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# setting the title of the surface
pygame.display.set_caption('Tutorial 1')

# creating a clock to keep track of time based events
clock = pygame.time.Clock()

# creating a new block object to play with
block = Block(x=375, y=290, height=10, width=70, color=WHITE)

# a flag to check the loop, else a lot of break statements are needed
run = True

# main game loop
while run:
    # setting FPS
    clock.tick(FPS)

    # handling events
    for event in pygame.event.get():  # iterating through event queue
        if event.type == pygame.QUIT:  # if event is a quit event
            run = False  # equivalent of saying break out of loop

        elif event.type == pygame.KEYDOWN:  # if any key is pressed down
            if event.key == pygame.K_ESCAPE:  # if escape key is pressed
                run = False  # break out of loop

            if event.key == pygame.K_SPACE:  # if space is pressed down
                # reset the position of the block
                block.x = 375  # set the x coordinate of the block as 100
                block.y = 290  # set the y coordinate of the block as 200

    """We can use the above technique to move our block too. But there is
    a drawback. If we keep holding the button down, the block will not continue
    to move. We have to press and release every time for the block to move
    (which is kinda irritating lol)
    """

    """Get a dictionary of all the buttons and whether they are pressed
    or not
    """
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:  # if right arrow is pressed
        block.x += block.vel

        """increment the x coordinate of the block by block.vel
        (which was set when initializing the class)
        So in this case, the block will move 20 pixels to the right.
        """
    elif keys[pygame.K_LEFT]:  # if left arrow is pressed
        block.x -= block.vel

        """Same logic, but here we are decreasing the value of
        x coordinate by 20

        Also, notice the use of 'elif'
        we use elif here as we can't move the block left and right
        at the same time.
        """

    if keys[pygame.K_UP]:  # if up arrow is pressed
        block.y -= block.vel

        """Decreasing the value of y coordinate will actually move
        the block upwards, as the screen is actually like 4th quadrant,
        with the top left corner sets a origin

        Notice the use of 'if' here
        Thus we can move the block in x direction and y direction
        at the same time.
        """

    elif keys[pygame.K_DOWN]:  # if down arrow is pressed
        block.y += block.vel  # same logic as above

        """increasing the y coordinate will move it down.
        """

    """So far we have changed the values of all the variable
    according to the events. Now we draw them to the surface.
    """

    """the below 3 lines can be put inside a function. As the number
    of objects increase, we need to draw/update a lot of items.
    """

    # drawing the background
    surface.fill(BLACK)

    # drawing the block on the surface
    block.draw_to_surface(surface)

    # updating the display for every iteration
    pygame.display.update()

# closing pygame, same way we initialized pygame
pygame.quit()
