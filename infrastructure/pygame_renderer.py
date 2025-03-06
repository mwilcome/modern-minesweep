import pygame
import math


class PygameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 50
        self.cell_font = pygame.font.SysFont('arial', 48)
        self.ui_font = pygame.font.SysFont('arial', 30)
        self.width, self.height = screen.get_size()

        # Colors
        self.background_start = (173, 216, 230)
        self.background_end = (70, 130, 180)
        self.cell_light = (220, 220, 220)
        self.cell_dark = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.grid_line_color = (200, 200, 200)
        self.flag_color = (0, 0, 255)
        self.mine_color = (255, 0, 0)
        self.revealed_color = (200, 200, 200)
        self.unrevealed_color = (150, 150, 150)

        # Background gradient
        self.background = self.create_gradient_surface()

        # UI Icons
        self.restart_icon = self.create_restart_icon()
        self.timer_icon = self.create_timer_icon()
        self.mine_icon = self.create_mine_icon()

        # UI Positions
        self.restart_rect = pygame.Rect(10, 5, 40, 40)
        self.timer_rect = pygame.Rect(self.width // 2 - 20, 5, 40, 40)
        self.mine_rect = pygame.Rect(self.width - 50, 5, 40, 40)

    def create_gradient_surface(self):
        surface = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            r = int(self.background_start[0] + (self.background_end[0] - self.background_start[0]) * y / self.height)
            g = int(self.background_start[1] + (self.background_end[1] - self.background_start[1]) * y / self.height)
            b = int(self.background_start[2] + (self.background_end[2] - self.background_start[2]) * y / self.height)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.width, y))
        return surface

    def create_restart_icon(self):
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.arc(icon, self.text_color, (0, 0, 32, 32), 0, 3.14, 2)
        pygame.draw.polygon(icon, self.text_color, [(16, 0), (20, 8), (12, 8)])
        return icon

    def create_timer_icon(self):
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(icon, self.text_color, (16, 16), 14, 2)
        pygame.draw.line(icon, self.text_color, (16, 16), (16, 10), 2)
        pygame.draw.line(icon, self.text_color, (16, 16), (22, 16), 2)
        return icon

    def create_mine_icon(self):
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(icon, self.text_color, (16, 16), 10)
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            x = 16 + 14 * math.cos(rad)
            y = 16 + 14 * math.sin(rad)
            pygame.draw.line(icon, self.text_color, (16, 16), (x, y), 2)
        return icon

    def render_ui(self, game, mouse_pos):
        """Render the UI with icons, timer, and hover effects."""
        # Restart button
        if self.restart_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.restart_rect.inflate(4, 4))
        self.screen.blit(self.restart_icon, (self.restart_rect.x + 4, self.restart_rect.y + 4))

        # Timer
        elapsed = game.get_elapsed_time()
        minutes = elapsed // 60
        seconds = elapsed % 60
        timer_text = self.ui_font.render(f"{minutes:02d}:{seconds:02d}", True, self.text_color)
        self.screen.blit(self.timer_icon, (self.timer_rect.x + 4, self.timer_rect.y + 4))
        self.screen.blit(timer_text, (self.timer_rect.right + 5, self.timer_rect.y + 5))

        # Mine counter (score for now)
        if self.mine_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.mine_rect.inflate(4, 4))
        self.screen.blit(self.mine_icon, (self.mine_rect.x + 4, self.mine_rect.y + 4))
        mine_text = self.ui_font.render(str(game.get_score()), True, self.text_color)
        self.screen.blit(mine_text, (self.mine_rect.left - 30, self.mine_rect.y + 5))

    def render(self, game, mouse_pos):
        """Render the game grid and UI."""
        self.screen.blit(self.background, (0, 0))
        self.render_ui(game, mouse_pos)

        # Render grid cells
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size + 50
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if cell.is_revealed:
                    if cell.is_mine:
                        pygame.draw.rect(self.screen, self.mine_color, rect)
                    else:
                        pygame.draw.rect(self.screen, self.revealed_color, rect)
                        if cell.adjacent_mines > 0:
                            text = self.cell_font.render(str(cell.adjacent_mines), True, self.text_color)
                            text_rect = text.get_rect(center=rect.center)
                            self.screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.screen, self.unrevealed_color, rect)
                if cell.is_flagged:
                    pygame.draw.circle(self.screen, self.flag_color, rect.center, 10)

        # Draw grid lines
        for i in range(game.cols + 1):
            x = i * self.cell_size
            pygame.draw.line(self.screen, self.grid_line_color, (x, 50), (x, 50 + game.rows * self.cell_size))
        for i in range(game.rows + 1):
            y = 50 + i * self.cell_size
            pygame.draw.line(self.screen, self.grid_line_color, (0, y), (game.cols * self.cell_size, y))

        # Hover effect
        grid_col = mouse_pos[0] // self.cell_size
        grid_row = (mouse_pos[1] - 50) // self.cell_size
        if 0 <= grid_row < game.rows and 0 <= grid_col < game.cols and not (game.game_over or game.won):
            x = grid_col * self.cell_size
            y = 50 + grid_row * self.cell_size
            pygame.draw.rect(self.screen, (255, 255, 0), (x, y, self.cell_size, self.cell_size), 2)

        # Win/Loss animations
        if game.game_over or game.won:
            self.render_game_end(game)

        pygame.display.flip()

    def render_game_end(self, game):
        """Render win or loss animation by revealing all mines."""
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size + 50
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if cell.is_mine:
                    if game.won:
                        # Win animation: Show all mines as flagged
                        pygame.draw.rect(self.screen, self.revealed_color, rect)
                        pygame.draw.circle(self.screen, self.flag_color, rect.center, 10)
                    else:
                        # Loss animation: Flash mines red
                        pygame.draw.rect(self.screen, self.mine_color, rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)  # White border for flash effect
        self.show_game_over(game.won)

    def show_game_over(self, won):
        """Display game over or win message."""
        message = "You Win!" if won else "Game Over!"
        text = self.cell_font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2,
                                50 + (self.height - 50) // 2 - text.get_height() // 2))
