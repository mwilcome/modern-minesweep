import pygame
import math


class PygameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.title_font = pygame.font.SysFont('arial', 50, bold=True)
        self.ui_font = pygame.font.SysFont('arial', 30)
        self.cell_font = pygame.font.SysFont('arial', 48)
        self.cell_size = 50
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
        self.background = self.create_gradient_surface()
        self.restart_icon = self.create_restart_icon()
        self.timer_icon = self.create_timer_icon()
        self.mine_icon = self.create_mine_icon()
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

    def render_menu(self, buttons, mouse_pos):
        self.screen.fill((240, 240, 240))
        title = self.title_font.render("Modern Minesweeper", True, (70, 130, 180))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        for button in buttons:
            button.draw(self.screen, self.ui_font, mouse_pos)
        pygame.display.flip()

    def render_ui(self, game, mouse_pos):
        if self.restart_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.restart_rect.inflate(4, 4))
        self.screen.blit(self.restart_icon, (self.restart_rect.x + 4, self.restart_rect.y + 4))
        elapsed = game.get_elapsed_time()
        minutes = elapsed // 60
        seconds = elapsed % 60
        timer_text = self.ui_font.render(f"{minutes:02d}:{seconds:02d}", True, self.text_color)
        self.screen.blit(self.timer_icon, (self.timer_rect.x + 4, self.timer_rect.y + 4))
        self.screen.blit(timer_text, (self.timer_rect.right + 5, self.timer_rect.y + 5))
        if self.mine_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 200, 0), self.mine_rect.inflate(4, 4))
        self.screen.blit(self.mine_icon, (self.mine_rect.x + 4, self.mine_rect.y + 4))
        mine_text = self.ui_font.render(str(game.get_score()), True, self.text_color)
        self.screen.blit(mine_text, (self.mine_rect.left - 30, self.mine_rect.y + 5))

    def render(self, game, mouse_pos):
        self.screen.blit(self.background, (0, 0))
        self.render_ui(game, mouse_pos)
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size + 50
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.line(self.screen, self.cell_light, (x, y), (x + self.cell_size, y))
                pygame.draw.line(self.screen, self.cell_light, (x, y), (x, y + self.cell_size))
                pygame.draw.line(self.screen, self.cell_dark, (x, y + self.cell_size - 1),
                                 (x + self.cell_size, y + self.cell_size - 1))
                pygame.draw.line(self.screen, self.cell_dark, (x + self.cell_size - 1, y),
                                 (x + self.cell_size - 1, y + self.cell_size))
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
        for i in range(game.cols + 1):
            x = i * self.cell_size
            pygame.draw.line(self.screen, self.grid_line_color, (x, 50), (x, 50 + game.rows * self.cell_size))
        for i in range(game.rows + 1):
            y = 50 + i * self.cell_size
            pygame.draw.line(self.screen, self.grid_line_color, (0, y), (game.cols * self.cell_size, y))
        if not (game.game_over or game.won):
            grid_col = mouse_pos[0] // self.cell_size
            grid_row = (mouse_pos[1] - 50) // self.cell_size
            if 0 <= grid_row < game.rows and 0 <= grid_col < game.cols:
                x = grid_col * self.cell_size
                y = 50 + grid_row * self.cell_size
                pygame.draw.rect(self.screen, (255, 255, 0), (x, y, self.cell_size, self.cell_size), 2)
        if game.game_over or game.won:
            self.render_game_end(game)
        pygame.display.flip()

    def render_game_end(self, game):
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size + 50
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if cell.is_mine:
                    if game.won:
                        pygame.draw.rect(self.screen, self.revealed_color, rect)
                        pygame.draw.circle(self.screen, self.flag_color, rect.center, 10)
                    else:
                        pygame.draw.rect(self.screen, self.mine_color, rect)
