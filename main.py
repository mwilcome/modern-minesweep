import pygame
from application.game_controller import GameController
from infrastructure.pygame_renderer import PygameRenderer


def main():
    pygame.init()
    screen_width = 500
    screen_height = 550
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Modern Minesweeper")
    renderer = PygameRenderer(screen)
    controller = GameController(10, 10, 10, renderer, screen_width)
    controller.run()


if __name__ == "__main__":
    main()
