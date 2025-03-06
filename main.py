import pygame
from application.game_controller import GameController
from infrastructure.pygame_renderer import PygameRenderer

pygame.init()
screen = pygame.display.set_mode((500, 550))  # Height increased by 50px for UI
pygame.display.set_caption("Minesweeper")

renderer = PygameRenderer(screen)
controller = GameController(10, 10, 10, renderer)  # 10x10 grid with 10 mines
controller.run()
