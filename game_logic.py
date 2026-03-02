class TicTacToe:
    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.winning_line = None
        self.is_draw = False
        self.mode = "PvP"  # Default mode

    def make_move(self, row, col):
        if self.winner or self.is_draw:
            return False

        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            winner_info = self.check_winner(row, col)
            if winner_info:
                self.winner = self.current_player
                self.winning_line = winner_info
            elif self.check_draw():
                self.is_draw = True
            else:
                self.switch_player()
            return True
        return False

    def ai_move(self):
        best_score = -float('inf')
        move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] is None:
                    self.board[r][c] = "O"
                    score = self.minimax(0, False)
                    self.board[r][c] = None
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        if move:
            self.make_move(move[0], move[1])

    def minimax(self, depth, is_maximizing):
        # Base cases
        winner_info = self.check_winner_logic()
        if winner_info == "O": return 10 - depth
        if winner_info == "X": return depth - 10
        if self.check_draw(): return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        self.board[r][c] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[r][c] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        self.board[r][c] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[r][c] = None
                        best_score = min(score, best_score)
            return best_score

    def check_winner_logic(self):
        # Simplified winner check for minimax
        for player in ["X", "O"]:
            # Rows/Cols
            for i in range(3):
                if all(self.board[i][j] == player for j in range(3)) or \
                   all(self.board[j][i] == player for j in range(3)):
                    return player
            # Diagonals
            if all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2-i] == player for i in range(3)):
                return player
        return None

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, row, col):
        player = self.board[row][col]
        # Check row
        if all(self.board[row][c] == player for c in range(3)):
            return ((row, 0), (row, 2))
        # Check column
        if all(self.board[r][col] == player for r in range(3)):
            return ((0, col), (2, col))
        # Check main diagonal
        if row == col:
            if all(self.board[i][i] == player for i in range(3)):
                return ((0, 0), (2, 2))
        # Check anti-diagonal
        if row + col == 2:
            if all(self.board[i][2-i] == player for i in range(3)):
                return ((0, 2), (2, 0))
        return None

    def check_draw(self):
        return all(all(cell is not None for cell in row) for row in self.board)

    def reset(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.winning_line = None
        self.is_draw = False
