import pygame
import random
from domain.value_objects.cell import Cell


class Game:
    def __init__(self, rows, cols, mine_count):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
        self.start_time = pygame.time.get_ticks()
        self.end_time = None
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        """Randomly place mines on the grid."""
        mines_placed = 0
        while mines_placed < self.mine_count:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if not self.grid[x][y].is_mine:
                self.grid[x][y].is_mine = True
                mines_placed += 1

    def _calculate_numbers(self):
        """Calculate the number of adjacent mines for each cell."""
        for x in range(self.rows):
            for y in range(self.cols):
                if not self.grid[x][y].is_mine:
                    count = sum(
                        1 for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                        if 0 <= x + dx < self.rows and 0 <= y + dy < self.cols
                        and self.grid[x + dx][y + dy].is_mine
                    )
                    self.grid[x][y].adjacent_mines = count

    def reveal_cell(self, row, col):
        """Reveal a cell and handle game logic."""
        if self.game_over or self.won:
            return
        cell = self.grid[row][col]
        if not cell.is_revealed and not cell.is_flagged:
            cell.is_revealed = True
            if cell.is_mine:
                self.game_over = True
                self.end_time = pygame.time.get_ticks()
            else:
                if cell.adjacent_mines == 0:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nr, nc = row + dx, col + dy
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                self.reveal_cell(nr, nc)
                self._check_win_condition()
                if self.won:
                    self.end_time = pygame.time.get_ticks()

    def _check_win_condition(self):
        """Check if all non-mine cells are revealed."""
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.won = True

    def get_elapsed_time(self):
        """Get the elapsed time in seconds."""
        if self.game_over or self.won:
            return (self.end_time - self.start_time) // 1000
        else:
            return (pygame.time.get_ticks() - self.start_time) // 1000

    def get_score(self):
        """Calculate the score based on correctly flagged mines."""
        return sum(1 for row in self.grid for cell in row if cell.is_mine and cell.is_flagged)
