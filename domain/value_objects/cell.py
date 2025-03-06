class Cell:
    def __init__(self):
        self.is_mine = False        # Whether the cell contains a mine
        self.is_revealed = False    # Whether the cell has been revealed
        self.is_flagged = False     # Whether the cell is flagged by the player
        self.adjacent_mines = 0     # Number of mines in adjacent cells

    def reveal(self):
        """Reveal the cell."""
        self.is_revealed = True

    def toggle_flag(self):
        """Toggle the flag status if the cell is not revealed."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
