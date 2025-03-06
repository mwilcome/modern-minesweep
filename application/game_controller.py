import pygame
from domain.entities.game import Game


class GameController:
    def __init__(self, rows, cols, mine_count, renderer):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.renderer = renderer
        self.reset_game()

    def reset_game(self):
        """Start a new game."""
        self.game = Game(self.rows, self.cols, self.mine_count)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game.game_over or self.game.won:
                        continue
                    mouse_x, mouse_y = event.pos
                    grid_row = mouse_y // 50  # 50px cell size
                    grid_col = mouse_x // 50
                    if 0 <= grid_row < self.game.rows and 0 <= grid_col < self.game.cols:
                        if event.button == 1:  # Left click
                            self.game.reveal_cell(grid_row, grid_col)
                        elif event.button == 3:  # Right click
                            self.game.grid[grid_row][grid_col].toggle_flag()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'R' to restart
                        self.reset_game()

            self.renderer.render(self.game)
            if self.game.game_over or self.game.won:
                self.renderer.show_game_over(self.game.won)
        pygame.quit()
