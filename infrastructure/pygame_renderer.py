import pygame


class PygameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 50  # Each cell is 50x50 pixels
        self.font = pygame.font.SysFont(None, 48)

    def render(self, game):
        """Render the game grid."""
        self.screen.fill((255, 255, 255))  # White background
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                if cell.is_revealed:
                    if cell.is_mine:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)  # Red for mines
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect)  # Light gray for revealed
                        if cell.adjacent_mines > 0:
                            text = self.font.render(str(cell.adjacent_mines), True, (0, 0, 0))
                            self.screen.blit(text, rect.center)
                else:
                    pygame.draw.rect(self.screen, (150, 150, 150), rect)  # Dark gray for unrevealed
                if cell.is_flagged:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, 10)  # Blue flag
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Black border
        pygame.display.flip()

    def show_game_over(self, won):
        """Display game over or win message."""
        message = "You Win!" if won else "Game Over!"
        text = self.font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2,
                                self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
