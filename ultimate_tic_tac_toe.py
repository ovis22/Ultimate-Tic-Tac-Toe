import sys
import enum
from typing import Union
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    BOARD_SIZE: int = 3
    WIN_REWARD: float = 1.0
    DRAW_REWARD: float = 0.0
    MAX_DEPTH: int = 2

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
    
    def finished(self) -> bool:
        return self.win(Player.PLAYER) or self.win(Player.OPPONENT) or self.draw()

    def make_move(self, row: int, col: int, player: Player) -> None:
        if self.board[row][col] != Cell.EMPTY:
            raise ValueError("Cell is already taken")
        self.board[row][col] = player

    def set_empty(self, row: int, col: int) -> None:
        self.board[row][col] = Cell.EMPTY

class UltimateBoard:
    def __init__(self) -> None:
        self.board: list[list[GameBoard]] = [
            [GameBoard() for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)
        ]
        self.next_board: tuple[int, int] | None = None

    def possible_moves(self) -> list[tuple[int, int]]:
        if self.next_board is not None and not self.board[self.next_board[0]][self.next_board[1]].finished():
            row, col = self.next_board
            moves: list[tuple[int, int]] = self.board[row][col].possible_moves()
            return [
                (row * Config.BOARD_SIZE + r, col * Config.BOARD_SIZE + c) for r, c in moves
            ]

        all_moves: list[tuple[int, int]] = []
        for row in range(Config.BOARD_SIZE):
            for col in range(Config.BOARD_SIZE):
                if not self.board[row][col].finished():
                    moves: list[tuple[int, int]] = self.board[row][col].possible_moves()
                    moves_converted: list[tuple[int, int]] = [
                        (row * Config.BOARD_SIZE + r, col * Config.BOARD_SIZE + c) for r, c in moves
                    ]
                    all_moves += moves_converted
        return all_moves

    def win(self, player: Player) -> bool:
        return any(
            all(self.board[i][j].win(player) for j in range(Config.BOARD_SIZE)) or
            all(self.board[j][i].win(player) for j in range(Config.BOARD_SIZE))
            for i in range(Config.BOARD_SIZE)
        ) or all(self.board[i][i].win(player) for i in range(Config.BOARD_SIZE)) or all(self.board[i][2 - i].win(player) for i in range(Config.BOARD_SIZE))

    def draw(self) -> bool:
        return not self.win(Player.PLAYER) and not self.win(Player.OPPONENT) and not self.possible_moves()

    def make_move(self, row: int, col: int, player: Player) -> None:
        board_row: int = int(row / 3)
        small_board_row: int = row % 3
        board_col: int = int(col / 3)
        small_board_col: int = col % 3
        self.board[board_row][board_col].make_move(small_board_row, small_board_col, player)
        self.next_board = (small_board_row, small_board_col)

    def set_empty(self, row: int, col: int) -> None:
        board_row: int = int(row / 3)
        small_board_row: int = row % 3
        board_col: int = int(col / 3)
        small_board_col: int = col % 3
        self.board[board_row][board_col].set_empty(small_board_row, small_board_col)

def score(game_board: UltimateBoard) -> float:
    # Sprawdz globalna wygrana
    if game_board.win(Player.PLAYER):
        return Config.WIN_REWARD * 1000
    if game_board.win(Player.OPPONENT):
        return -Config.WIN_REWARD * 1000
    
    total_score = 0.0
    
    # Ocen kazda mala plansze
    for r in range(Config.BOARD_SIZE):
        for c in range(Config.BOARD_SIZE):
            small_board = game_board.board[r][c]
            board_score = 0.0
            
            if small_board.win(Player.PLAYER):
                board_score = 10.0
            elif small_board.win(Player.OPPONENT):
                board_score = -10.0
            else:
                # Heurystyka dla niedokonczonej malej planszy
                # Zachecaj do zajmowania srodka
                if small_board.board[1][1] == Player.PLAYER:
                    board_score += 0.5
                elif small_board.board[1][1] == Player.OPPONENT:
                    board_score -= 0.5
            
            # Wagi dla malych plansz (Srodek jest najwazniejszy, potem rogi)
            weight = 1.0
            if r == 1 and c == 1:
                weight = 2.0
            elif (r + c) % 2 == 0: # Rogi
                weight = 1.2
            
            total_score += board_score * weight

    return total_score

def minimax(game_board: UltimateBoard, player: Player, alpha: float, beta: float, depth: int) -> tuple[float, tuple[int, int] | None]:
    if depth == 0 or game_board.win(Player.PLAYER) or game_board.win(Player.OPPONENT) or game_board.draw():
        return score(game_board), None

    moves = game_board.possible_moves()
    # Sortuj ruchy wedlug prostej heurystyki, aby poprawic odcinanie? 
    # Na razie prosta iteracja.
    
    best_move = None
    
    if player == Player.PLAYER:
        max_eval = -float("inf")
        for move in moves:
            # Sklonowac plansze czy cofnac ruch? 
            # Poniewaz make_move modyfikuje stan, MUSIMY go cofnac.
            # Musimy sledzic poprzedni stan 'next_board', aby cofnac poprawnie.
            
            # Zapisywanie stanu
            prev_next_board = game_board.next_board
            row, col = move
            # make_move modyfikuje komorke i aktualizuje next_board
            game_board.make_move(row, col, player)
            
            eval_score, _ = minimax(game_board, player.opponent(), alpha, beta, depth - 1)
            
            # Cofanie stanu
            game_board.set_empty(row, col)
            game_board.next_board = prev_next_board
            
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
            prev_next_board = game_board.next_board
            row, col = move
            game_board.make_move(row, col, player)
            
            eval_score, _ = minimax(game_board, player.opponent(), alpha, beta, depth - 1)
            
            game_board.set_empty(row, col)
            game_board.next_board = prev_next_board
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def game_loop() -> None:
    game_board: UltimateBoard = UltimateBoard()
    while True:
        try:
            line = input().split()
            if not line: break
            opponent_row, opponent_col = [int(i) for i in line]
            valid_action_count = int(input())
            for _ in range(valid_action_count):
                input()
        except EOFError: break

        if opponent_row != -1:
            game_board.make_move(opponent_row, opponent_col, Player.OPPONENT)

        _, move = minimax(game_board, Player.PLAYER, -float("inf"), float("inf"), depth=Config.MAX_DEPTH)
        
        if move:
            row, col = move
            game_board.make_move(row, col, Player.PLAYER)
            print(f"{row} {col}")
        else:
            print("0 0")

if __name__ == "__main__":
    game_loop()
