import pygame
import math  # Import math for trigonometric functions


class PygameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 50
        self.cell_font = pygame.font.SysFont('arial', 48)  # Explicit font to avoid warnings
        self.ui_font = pygame.font.SysFont('arial', 30)
        self.width, self.height = screen.get_size()

        # Colors for light theme
        self.background_start = (173, 216, 230)  # Light blue
        self.background_end = (70, 130, 180)  # Steel blue
        self.cell_light = (220, 220, 220)  # Light border for bevel
        self.cell_dark = (100, 100, 100)  # Dark border for bevel
        self.text_color = (0, 0, 0)  # Black text

        # Create background surface with gradient
        self.background = self.create_gradient_surface()

        # UI Icons (simple shapes)
        self.restart_icon = self.create_restart_icon()
        self.timer_icon = self.create_timer_icon()
        self.mine_icon = self.create_mine_icon()

        # UI Positions
        self.restart_rect = pygame.Rect(10, 5, 40, 40)
        self.timer_rect = pygame.Rect(self.width // 2 - 20, 5, 40, 40)
        self.mine_rect = pygame.Rect(self.width - 50, 5, 40, 40)

    def create_gradient_surface(self):
        """Create a surface with a vertical gradient."""
        surface = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            r = int(self.background_start[0] + (self.background_end[0] - self.background_start[0]) * y / self.height)
            g = int(self.background_start[1] + (self.background_end[1] - self.background_start[1]) * y / self.height)
            b = int(self.background_start[2] + (self.background_end[2] - self.background_start[2]) * y / self.height)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.width, y))
        return surface

    def create_restart_icon(self):
        """Create a simple restart icon (circular arrow)."""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.arc(icon, self.text_color, (0, 0, 32, 32), 0, 3.14, 2)
        pygame.draw.polygon(icon, self.text_color, [(16, 0), (20, 8), (12, 8)])  # Arrowhead
        return icon

    def create_timer_icon(self):
        """Create a simple timer icon (clock)."""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(icon, self.text_color, (16, 16), 14, 2)
        pygame.draw.line(icon, self.text_color, (16, 16), (16, 10), 2)  # Hour hand
        pygame.draw.line(icon, self.text_color, (16, 16), (22, 16), 2)  # Minute hand
        return icon

    def create_mine_icon(self):
        """Create a simple mine icon (circle with spikes)."""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(icon, self.text_color, (16, 16), 10)
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            x = 16 + 14 * math.cos(rad)  # Use math.cos instead of pygame.math.cos
            y = 16 + 14 * math.sin(rad)  # Use math.sin instead of pygame.math.sin
            pygame.draw.line(icon, self.text_color, (16, 16), (x, y), 2)
        return icon

    def render_ui(self, score, mouse_pos):
        """Render the UI with icons and hover effects."""
        # Restart button
        if self.restart_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.restart_rect.inflate(4, 4))  # Hover effect
        self.screen.blit(self.restart_icon, (self.restart_rect.x + 4, self.restart_rect.y + 4))

        # Timer (placeholder)
        if self.timer_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.timer_rect.inflate(4, 4))
        self.screen.blit(self.timer_icon, (self.timer_rect.x + 4, self.timer_rect.y + 4))
        timer_text = self.ui_font.render("00:00", True, self.text_color)
        self.screen.blit(timer_text, (self.timer_rect.right + 5, self.timer_rect.y + 5))

        # Mine counter (using score as placeholder)
        if self.mine_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.mine_rect.inflate(4, 4))
        self.screen.blit(self.mine_icon, (self.mine_rect.x + 4, self.mine_rect.y + 4))
        mine_text = self.ui_font.render(str(score), True, self.text_color)
        self.screen.blit(mine_text, (self.mine_rect.left - 30, self.mine_rect.y + 5))

    def render(self, game, mouse_pos):
        """Render the game grid and UI."""
        self.screen.blit(self.background, (0, 0))  # Draw gradient background

        # Render UI
        self.render_ui(game.get_score(), mouse_pos)

        # Render grid with beveled cells
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size + 50  # Offset for UI
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # Bevel effect
                pygame.draw.line(self.screen, self.cell_light, (x, y), (x + self.cell_size, y))  # Top
                pygame.draw.line(self.screen, self.cell_light, (x, y), (x, y + self.cell_size))  # Left
                pygame.draw.line(self.screen, self.cell_dark, (x, y + self.cell_size - 1),
                                 (x + self.cell_size, y + self.cell_size - 1))  # Bottom
                pygame.draw.line(self.screen, self.cell_dark, (x + self.cell_size - 1, y),
                                 (x + self.cell_size - 1, y + self.cell_size))  # Right

                # Cell content
                if cell.is_revealed:
                    if cell.is_mine:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect)
                        if cell.adjacent_mines > 0:
                            text = self.cell_font.render(str(cell.adjacent_mines), True, self.text_color)
                            text_rect = text.get_rect(center=rect.center)
                            self.screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.screen, (150, 150, 150), rect)
                if cell.is_flagged:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, 10)

        pygame.display.flip()

    def show_game_over(self, won):
        """Display game over or win message."""
        message = "You Win!" if won else "Game Over!"
        text = self.cell_font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2,
                                50 + (self.height - 50) // 2 - text.get_height() // 2))
        pygame.display.flip()
