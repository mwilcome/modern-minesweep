import pygame
from domain.entities.game import Game


class GameController:
    def __init__(self, rows, cols, mine_count, renderer):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.renderer = renderer
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound('click.wav')
        self.flag_sound = pygame.mixer.Sound('flag.wav')
        self.win_sound = pygame.mixer.Sound('win.wav')
        self.lose_sound = pygame.mixer.Sound('lose.wav')
        self.reset_game()

    def reset_game(self):
        """Start a new game."""
        self.game = Game(self.rows, self.cols, self.mine_count)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 5 <= mouse_y <= 45 and 10 <= mouse_x <= 50:
                        self.reset_game()
                    elif not self.game.game_over and not self.game.won:
                        grid_row = (mouse_y - 50) // 50
                        grid_col = mouse_x // 50
                        if 0 <= grid_row < self.rows and 0 <= grid_col < self.cols:
                            if event.button == 1:  # Left click
                                game_ended = self.game.reveal_cell(grid_row, grid_col)
                                if game_ended == 'lose':
                                    self.lose_sound.play()
                                elif game_ended == 'win':
                                    self.win_sound.play()
                                else:
                                    self.click_sound.play()
                            elif event.button == 3:  # Right click
                                self.game.grid[grid_row][grid_col].toggle_flag()
                                self.flag_sound.play()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()

            self.renderer.render(self.game, mouse_pos)
        pygame.quit()
