import pygame


class PygameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 50
        self.cell_font = pygame.font.SysFont(None, 48)  # Font for grid numbers
        self.ui_font = pygame.font.SysFont(None, 30)  # Smaller font for UI

    def render_ui(self, score):
        """Render the UI with a restart button and score display."""
        # Restart button
        restart_rect = pygame.Rect(10, 5, 100, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), restart_rect)  # Green button
        restart_text = self.ui_font.render("Restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)  # Center text in button
        self.screen.blit(restart_text, restart_text_rect)

        # Score display, aligned to the right
        score_text = self.ui_font.render(f"Score: {score}", True, (0, 0, 0))
        score_text_rect = score_text.get_rect(right=490, top=10)  # Right-aligned with margin
        self.screen.blit(score_text, score_text_rect)

    def render(self, game):
        """Render the game grid and UI."""
        self.screen.fill((255, 255, 255))  # White background
        self.render_ui(game.get_score())  # Render UI first

        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size + 50, self.cell_size, self.cell_size)
                if cell.is_revealed:
                    if cell.is_mine:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)  # Red for mines
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect)  # Light gray for revealed
                        if cell.adjacent_mines > 0:
                            text = self.cell_font.render(str(cell.adjacent_mines), True, (0, 0, 0))
                            text_rect = text.get_rect(center=rect.center)
                            self.screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.screen, (150, 150, 150), rect)  # Dark gray for unrevealed
                if cell.is_flagged:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, 10)  # Blue flag
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Black border
        pygame.display.flip()

    def show_game_over(self, won):
        """Display game over or win message centered in the grid area."""
        message = "You Win!" if won else "Game Over!"
        text = self.cell_font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2,
                                50 + (500 // 2) - text.get_height() // 2))  # Centered in grid area
        pygame.display.flip()
