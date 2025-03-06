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
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position for hover effects
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Check if restart button is clicked (top-left corner)
                    if 5 <= mouse_y <= 45 and 10 <= mouse_x <= 50:
                        self.reset_game()
                    elif not self.game.game_over and not self.game.won:
                        # Adjust for UI offset (50px from top)
                        grid_row = (mouse_y - 50) // 50
                        grid_col = mouse_x // 50
                        if 0 <= grid_row < self.rows and 0 <= grid_col < self.cols:
                            if event.button == 1:  # Left click
                                self.game.reveal_cell(grid_row, grid_col)
                            elif event.button == 3:  # Right click
                                self.game.grid[grid_row][grid_col].toggle_flag()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'R' to restart
                        self.reset_game()

            # Render the game state
            if self.game.game_over or self.game.won:
                self.renderer.show_game_over(self.game.won)
            else:
                self.renderer.render(self.game, mouse_pos)

        pygame.quit()
