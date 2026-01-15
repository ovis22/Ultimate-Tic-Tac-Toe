import sys
import enum
from typing import Union
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    BOARD_SIZE: int = 3
    WIN_REWARD: float = 1.0
    DRAW_REWARD: float = 0.0

class Player(enum.Enum):
    OPPONENT = enum.auto()
    PLAYER = enum.auto()

    def opponent(self) -> 'Player':
        return Player.OPPONENT if self == Player.PLAYER else Player.PLAYER

class Cell(enum.Enum):
    EMPTY = enum.auto()

CellState = Union[Cell, Player]

class GameBoard:
    def __init__(self) -> None:
        self.board: list[list[CellState]] = [
            [Cell.EMPTY for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)
        ]

    def possible_moves(self) -> list[tuple[int, int]]:
        if self.win(Player.OPPONENT) or self.win(Player.PLAYER):
            return []
        return [
            (r, c)
            for r in range(Config.BOARD_SIZE)
            for c in range(Config.BOARD_SIZE)
            if self.board[r][c] == Cell.EMPTY
        ]

    def win(self, player: Player) -> bool:
        return any(
            all(self.board[i][j] == player for j in range(Config.BOARD_SIZE)) or
            all(self.board[j][i] == player for j in range(Config.BOARD_SIZE))
            for i in range(Config.BOARD_SIZE)
        ) or all(self.board[i][i] == player for i in range(Config.BOARD_SIZE)) or all(self.board[i][2 - i] == player for i in range(Config.BOARD_SIZE))

    def draw(self) -> bool:
        return not self.win(Player.PLAYER) and not self.win(Player.OPPONENT) and not self.possible_moves()

    def make_move(self, row: int, col: int, player: Player) -> None:
        if self.board[row][col] != Cell.EMPTY:
            raise ValueError("Cell is already taken")
        self.board[row][col] = player

    def set_empty(self, row: int, col: int) -> None:
        self.board[row][col] = Cell.EMPTY

def minimax(game_board: GameBoard, player: Player, alpha: float, beta: float) -> tuple[float, tuple[int, int] | None]:
    if game_board.win(Player.PLAYER):
        return Config.WIN_REWARD, None
    if game_board.win(Player.OPPONENT):
        return -Config.WIN_REWARD, None
    if game_board.draw():
        return Config.DRAW_REWARD, None

    moves = game_board.possible_moves()
    best_move = None

    if player == Player.PLAYER:
        max_eval = -float("inf")
        for move in moves:
            game_board.make_move(move[0], move[1], player)
            eval_score, _ = minimax(game_board, player.opponent(), alpha, beta)
            game_board.set_empty(move[0], move[1])
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in moves:
            game_board.make_move(move[0], move[1], player)
            eval_score, _ = minimax(game_board, player.opponent(), alpha, beta)
            game_board.set_empty(move[0], move[1])
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def game_loop() -> None:
    game_board: GameBoard = GameBoard()
    while True:
        try:
            line = input().split()
            if not line: break
            opponent_row, opponent_col = [int(i) for i in line]
            valid_action_count = int(input())
            for _ in range(valid_action_count):
                input() # Wczytaj linie poprawnych ruchow
        except EOFError:
            break

        if opponent_row != -1:
            game_board.make_move(opponent_row, opponent_col, Player.OPPONENT)

        # Obliczenia Minimax
        _, move = minimax(game_board, Player.PLAYER, -float("inf"), float("inf"))
        
        if move:
            row, col = move
            game_board.make_move(row, col, Player.PLAYER)
            print(f"{row} {col}")
        else:
            print("0 0") # Ruch awaryjny, jesli nie znaleziono innego (koniec gry)

if __name__ == "__main__":
    game_loop()
