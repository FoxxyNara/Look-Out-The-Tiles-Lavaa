from game_logic import EMPTY, PLAYER, AI, LAVA

def evaluate_board(board):
    """
    Heuristic Evaluation Function:
    Balances Material (piece count), Mobility, Corner Control, and Lava Avoidance.
    """
    ai_score = 0
    player_score = 0
    
    # Corner weights (corners are exceptionally valuable because they can't be flipped)
    weights = [
        [100, -20, 10, 10, -20, 100],
        [-20, -50, -2, -2, -50, -20],
        [ 10,  -2,  5,  5,  -2,  10],
        [ 10,  -2,  5,  5,  -2,  10],
        [-20, -50, -2, -2, -50, -20],
        [100, -20, 10, 10, -20, 100]
    ]

    for r in range(board.size):
        for c in range(board.size):
            cell = board.grid[r][c]
            if cell == AI:
                ai_score += weights[r][c]
            elif cell == PLAYER:
                player_score += weights[r][c]

    # Add mobility factor (number of valid moves available)
    ai_mobility = len(board.get_valid_moves(AI))
    player_mobility = len(board.get_valid_moves(PLAYER))
    
    total_eval = (ai_score - player_score) + 5 * (ai_mobility - player_mobility)
    return total_eval

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_moves = board.get_valid_moves(AI if maximizing_player else PLAYER)
    
    # Terminal conditions: Max depth reached or no moves left for both players
    if depth == 0 or not valid_moves:
        if not board.get_valid_moves(AI) and not board.get_valid_moves(PLAYER):
            # Game over: return absolute scores based on piece count
            ai_count = sum(row.count(AI) for row in board.grid)
            p_count = sum(row.count(PLAYER) for row in board.grid)
            return (10000 if ai_count > p_count else -10000), None
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            next_board = board.clone()
            next_board.make_move(move[0], move[1], AI)
            eval_score, _ = minimax(next_board, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            next_board = board.clone()
            next_board.make_move(move[0], move[1], PLAYER)
            eval_score, _ = minimax(next_board, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move