import os
import pygame
import random
import settings as s
# from sprites import *


class CoronaBreakout:

    def __init__(self):
        """Initializing attributes for a new game.
        """

        pygame.init()
        pygame.mixer.init()
        self.load_data()

        self.screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
        pygame.display.set_caption(s.TITLE)

        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(s.FONT_NAME)
        self.running = True

    def load_data(self):
        """Loads all necessary data.

        Highscore, spritesheets, images, sounds.
        """

        self.dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.dir, 'images')
        self.sound_dir = os.path.join(self.dir, 'sounds')

        # load high score, maybe try using json for each level.
        try:
            # if file exists, load data
            with open(os.path.join(self.dir, s.HS_FILE), 'r') as f:
                self.highscore = int(f.read())
            # else create new file and initialize highscore to 0
        except Exception:
            with open(os.path.join(self.dir, s.HS_FILE), 'w') as f:
                self.highscore = 0

        # load spritesheets

        # load images

        # load sounds

    def new(self):
        """Start a new game.
        """

        self.score = 0

        # initialize sprite groups

        # create new instance of player

        # create new platforms

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

            # mouse click on start screen

            # escape key to pause

            # keydown space to jump

            # keyup space to jump_cut

    def update(self):
        """Updates attributes of objects.

        Main logic of the game.
        """

        # update all sprites
        pass

    def draw(self):
        """Draw updated objects to the screen.
        """

        self.screen.fill(s.BGCOLOR)

        # draw all sprites

        # draw texts

        pygame.display.update()

    def show_start_screen(self):
        """Start screen of the game.

        Main menu of the game.
        """

        # load music

        self.screen.fill(s.BGCOLOR)

        # draw texts/buttons

        pygame.display.update()

        # fadeout music

    def show_gameover_screen(self):
        """Game over screen.

        Renders user's score and highscore.
        """

        if not self.running:
            return None

        # load music

        self.screen.fill(s.BGCOLOR)

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

    def show_levels_screen(self):
        """Levels screen.
        """

        pass

    def show_pause_screen(self):
        """Pause screen.
        """

        pass

    def wait_for_key(self):
        """Wait for key press.
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
        text_surface = font.render(text, True, color)
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
