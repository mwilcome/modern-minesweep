class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def toggle_flag(self):
        """Toggle the flag state if the cell isn’t revealed."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
