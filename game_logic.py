import random

EMPTY = 0
PLAYER = 1  
AI = 2      
LAVA = -1   

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

class Board:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.turn_counter = 0  # Tracks back and forth pairs of turns
        
        mid = size // 2
        self.grid[mid-1][mid-1] = AI
        self.grid[mid][mid] = AI
        self.grid[mid-1][mid] = PLAYER
        self.grid[mid][mid-1] = PLAYER

    def is_valid_position(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def get_valid_moves(self, player):
        valid_moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == EMPTY:
                    flips = self._get_flips(r, c, player)
                    if flips:
                        valid_moves.append((r, c))
        return valid_moves

    def _get_flips(self, r, c, player):
        if self.grid[r][c] != EMPTY:
            return []
        
        opponent = PLAYER if player == AI else AI
        total_flips = []

        for dr, dc in DIRECTIONS:
            temp_path = []
            while self.is_valid_position(r + dr * (len(temp_path) + 1), c + dc * (len(temp_path) + 1)):
                next_r = r + dr * (len(temp_path) + 1)
                next_c = c + dc * (len(temp_path) + 1)
                
                if self.grid[next_r][next_c] == opponent:
                    temp_path.append((next_r, next_c))
                elif self.grid[next_r][next_c] == player:
                    if temp_path:
                        total_flips.extend(temp_path)
                    break
                else:
                    break
                    
        return total_flips

    def make_move(self, r, c, player, is_ai_turn=False):
        flips = self._get_flips(r, c, player)
        if not flips:
            return False

        self.grid[r][c] = player
        for fr, fc in flips:
            self.grid[fr][fc] = player

        # If it's the AI's turn, it completes a full round (Player + AI)
        if is_ai_turn:
            self.turn_counter += 1
            # Every 2 rounds, trigger lava drop!
            if self.turn_counter >= 2:
                self.trigger_lava()
                self.turn_counter = 0  # Reset counter

        return True

    def trigger_lava(self):
        empty_spots = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == EMPTY]
        if empty_spots:
            num_to_burn = min(2, len(empty_spots))
            burned = random.sample(empty_spots, num_to_burn)
            for br, bc in burned:
                self.grid[br][bc] = LAVA

    def clone(self):
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        new_board.turn_counter = self.turn_counter
        return new_board