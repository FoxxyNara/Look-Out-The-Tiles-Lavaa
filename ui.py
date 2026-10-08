import tkinter as tk
from tkinter import messagebox
from game_logic import Board, EMPTY, PLAYER, AI, LAVA
from ai import minimax

class LavaaOthello:
    def __init__(self, root):
        self.root = root
        self.root.title("Look Out! The Tile's Lavaa!")
        self.board = Board(size=6)
        
        self.cell_size = 80
        self.canvas = tk.Canvas(root, width=self.board.size * self.cell_size, height=self.board.size * self.cell_size, bg="#2c3e50")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.status_label = tk.Label(root, text="Your Turn (Black)", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.board.size):
            for c in range(self.board.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                fill_color = "#27ae60"
                cell_value = self.board.grid[r][c]
                
                if cell_value == LAVA:
                    fill_color = "#c0392b"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#1e272e", width=2)
                
                if cell_value == PLAYER:
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill="#111111")
                elif cell_value == AI:
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill="#ecf0f1")
                elif cell_value == LAVA:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text="🔥", font=("Arial", 24))

        # Highlight valid moves for human
        valid_moves = self.board.get_valid_moves(PLAYER)
        for r, c in valid_moves:
            x1 = c * self.cell_size + 30
            y1 = r * self.cell_size + 30
            x2 = x1 + 20
            y2 = y1 + 20
            self.canvas.create_oval(x1, y1, x2, y2, fill="#f1c40f", outline="")

    def handle_click(self, event):
        c = event.x // self.cell_size
        r = event.y // self.cell_size

        valid_moves = self.board.get_valid_moves(PLAYER)
        
        # If player has no valid moves, force pass their turn to the AI
        if not valid_moves:
            messagebox.showinfo("Pass Turn", "No valid moves available! Your turn is skipped.")
            if self.check_game_over():
                return
            self.status_label.config(text="AI's Turn (White) - Thinking...")
            self.root.after(500, self.ai_turn)
            return

        if (r, c) in valid_moves:
            self.board.make_move(r, c, PLAYER)
            self.draw_board()
            
            if self.check_game_over():
                return

            # AI Turn
            self.status_label.config(text="AI's Turn (White) - Thinking...")
            self.root.after(500, self.ai_turn)

    def ai_turn(self):
        ai_moves = self.board.get_valid_moves(AI)
        
        if ai_moves:
            _, best_move = minimax(self.board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
            if best_move:
                # Pass True here because the AI's move closes out the round
                self.board.make_move(best_move[0], best_move[1], AI, is_ai_turn=True)
        else:
            messagebox.showinfo("Pass Turn", "AI has no valid moves! AI's turn is skipped.")

        self.draw_board()
        
        if not self.check_game_over():
            if not self.board.get_valid_moves(PLAYER):
                messagebox.showinfo("Pass Turn", "You still have no valid moves. Passing back to AI...")
                self.root.after(500, self.ai_turn)
            else:
                self.status_label.config(text="Your Turn (Black) - Watch out for Lava every 2 rounds!")

    def check_game_over(self):
        p_moves = self.board.get_valid_moves(PLAYER)
        ai_moves = self.board.get_valid_moves(AI)
        
        if not p_moves and not ai_moves:
            p_count = sum(row.count(PLAYER) for row in self.board.grid)
            ai_count = sum(row.count(AI) for row in self.board.grid)
            
            msg = f"Game Over!\nPlayer (Black): {p_count}\nAI (White): {ai_count}\n\n"
            if p_count > ai_count:
                msg += "You Win!"
            elif ai_count > p_count:
                msg += "AI Wins!"
            else:
                msg += "It's a Draw!"
                
            self.status_label.config(text="Game Over")
            messagebox.showinfo("Corner Clash - Game Over", msg)
            return True
        return False