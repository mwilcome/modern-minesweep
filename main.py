import pygame
from application.game_controller import GameController
from infrastructure.pygame_renderer import PygameRenderer


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 550))
    pygame.display.set_caption("Minesweeper")
    renderer = PygameRenderer(screen)
    controller = GameController(10, 10, 10, renderer)
    controller.run()


if __name__ == "__main__":
    main()
