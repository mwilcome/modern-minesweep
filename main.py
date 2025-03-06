import pygame
from application.game_controller import GameController
from infrastructure.pygame_renderer import PygameRenderer

# Initialize Pygame
pygame.init()

# Set up the screen (adjust size as needed)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Modern Minesweeper")

# Create renderer and game controller
renderer = PygameRenderer(screen)
controller = GameController(10, 10, 10, renderer)  # 10x10 grid with 10 mines

# Run the game
controller.run()
