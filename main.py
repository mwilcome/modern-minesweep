import pygame
from application.game_controller import GameController
from infrastructure.pygame_renderer import PygameRenderer

pygame.init()
screen = pygame.display.set_mode((500, 500))  # 10x10 grid with 50px cells
pygame.display.set_caption("Minesweeper")

renderer = PygameRenderer(screen)
controller = GameController(10, 10, 10, renderer)  # 10x10 grid with 10 mines
controller.run()
