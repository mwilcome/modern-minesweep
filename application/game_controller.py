import pygame
from domain.entities.game import Game


class Button:
    def __init__(self, x, y, width, height, text, on_click):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click

    def draw(self, screen, font, mouse_pos):
        color = (100, 160, 210) if self.rect.collidepoint(mouse_pos) else (70, 130, 180)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=self.rect.center))


class GameController:
    def __init__(self, rows, cols, mine_count, renderer, screen_width):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.renderer = renderer
        self.screen_width = screen_width
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound('click.wav')
        self.flag_sound = pygame.mixer.Sound('flag.wav')
        self.win_sound = pygame.mixer.Sound('win.wav')
        self.lose_sound = pygame.mixer.Sound('lose.wav')
        self.state = "menu"
        self.menu_buttons = self.create_menu_buttons()
        self.game = None

    def create_menu_buttons(self):
        buttons = []
        button_width = 150
        center_x = self.screen_width // 2 - button_width // 2
        buttons.append(Button(center_x, 200, button_width, 50, "New Game", self.start_game))
        buttons.append(Button(center_x, 270, button_width, 50, "Quit", self.quit_game))
        return buttons

    def start_game(self):
        """Initialize or reset the game."""
        self.game = Game(self.rows, self.cols, self.mine_count)
        self.state = "game"

    def quit_game(self):
        pygame.quit()
        exit()

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "menu":
                        for button in self.menu_buttons:
                            if button.rect.collidepoint(event.pos):
                                button.on_click()
                    elif self.state == "game" and self.game:
                        # Check restart button in all game states
                        if self.renderer.restart_rect.collidepoint(event.pos):
                            self.start_game()
                        elif not (self.game.game_over or self.game.won):
                            grid_row = (event.pos[1] - 50) // 50
                            grid_col = event.pos[0] // 50
                            if 0 <= grid_row < self.rows and 0 <= grid_col < self.cols:
                                if event.button == 1:
                                    result = self.game.reveal_cell(grid_row, grid_col)
                                    if result == 'lose':
                                        self.lose_sound.play()
                                    elif result == 'win':
                                        self.win_sound.play()
                                    else:
                                        self.click_sound.play()
                                elif event.button == 3:
                                    self.game.grid[grid_row][grid_col].toggle_flag()
                                    self.flag_sound.play()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart regardless of state
                        if self.state == "game":
                            self.start_game()
                        else:
                            self.quit_game()

            if self.state == "menu":
                self.renderer.render_menu(self.menu_buttons, mouse_pos)
            elif self.state == "game" and self.game:
                self.renderer.render(self.game, mouse_pos)

        pygame.quit()
