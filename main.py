import pygame
import settings as s
from game import CoronaBreakout

if __name__ == '__main__':
    # initializing an instance of the game.
    game = CoronaBreakout()
    game.show_start_screen()
    game.show_intro_scene()
    game.show_mission_screen()

    while game.running:

        for i in range(1, s.GAME_LEVELS + 1):
            game.show_level_intro(level=i)
            game.new()

            if game.failed:
                break

        if not game.failed:
            game.show_completed_screen()

        game.show_gameover_screen()

    pygame.quit()
