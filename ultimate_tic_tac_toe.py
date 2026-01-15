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
    
    def finished(self) -> bool:
        return self.win(Player.PLAYER) or self.win(Player.OPPONENT) or self.draw()

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

import time

def score(game_board: UltimateBoard, player: Player) -> float:
    # 1. Sprawdz globalna wygrana/przegrana
    if game_board.win(player):
        return 10000.0
    if game_board.win(player.opponent()):
        return -10000.0
    
    total_score = 0.0
    
    # 2. Ocen kontrole nad duza plansza (wagi strategiczne)
    # 0 1 2
    # 3 4 5
    # 6 7 8
    # Srodek (4) najważniejszy, potem rogi (0,2,6,8)
    big_board_weights = [
        1.2, 1.0, 1.2,
        1.0, 2.0, 1.0,
        1.2, 1.0, 1.2
    ]
    
    for r in range(Config.BOARD_SIZE):
        for c in range(Config.BOARD_SIZE):
            small_board = game_board.board[r][c]
            weight = big_board_weights[r * 3 + c]
            
            # Jesli mala plansza zdobyta - ogromny bonus
            if small_board.win(player):
                total_score += 100.0 * weight
            elif small_board.win(player.opponent()):
                total_score -= 100.0 * weight
            else:
                # 3. Ocen stan malej planszy (Heurystyka)
                # Policz znaki na malej planszy
                player_marks = 0
                opponent_marks = 0
                
                # Sprawdz linie "prawie wygrane" (Optymalizacja dla Ligi Zlotej)
                lines = []
                # Wiersze
                for i in range(3): lines.append([small_board.board[i][j] for j in range(3)])
                # Kolumny
                for j in range(3): lines.append([small_board.board[i][j] for i in range(3)])
                # Przekatne
                lines.append([small_board.board[i][i] for i in range(3)])
                lines.append([small_board.board[i][2-i] for i in range(3)])
                
                for line in lines:
                   p_cnt = sum(1 for cell in line if cell == player)
                   o_cnt = sum(1 for cell in line if cell == player.opponent())
                   
                   if p_cnt == 2 and o_cnt == 0:
                       total_score += 5.0 * weight # Prawie wygrana mala plansza
                   elif o_cnt == 2 and p_cnt == 0:
                       total_score -= 5.0 * weight # Zagrozenie

                for sr in range(Config.BOARD_SIZE):
                    for sc in range(Config.BOARD_SIZE):
                        cell = small_board.board[sr][sc]
                        if cell == player:
                            player_marks += 1
                        elif cell == player.opponent():
                            opponent_marks += 1
                
                # Male punkty za sama obecnosc (kontrola srodka)
                total_score += (player_marks - opponent_marks) * weight
                
                # Bonus za zajecie srodka malej planszy
                if small_board.board[1][1] == player:
                    total_score += 2.0 * weight
                elif small_board.board[1][1] == player.opponent():
                    total_score -= 2.0 * weight

    return total_score

def minimax(game_board: UltimateBoard, player: Player, alpha: float, beta: float, depth: int, start_time: float, time_limit: float) -> tuple[float, tuple[int, int] | None]:
    # Sprawdzenie czasu
    if (time.time() - start_time) > time_limit:
        raise TimeoutError()
        
    if depth == 0 or game_board.finished():
        return score(game_board, Player.PLAYER), None

    moves = game_board.possible_moves()
    # Optymalizacja: Brak ruchow (powinno byc pokryte przez finished, ale dla bezpieczenstwa)
    if not moves:
        return score(game_board, Player.PLAYER), None

    best_move = moves[0]
    
    if player == Player.PLAYER:
        max_eval = -float("inf")
        for move in moves:
            # Zapisz stan
            prev_next_board = game_board.next_board
            row, col = move
            game_board.make_move(row, col, player)
            
            try:
                eval_score, _ = minimax(game_board, player.opponent(), alpha, beta, depth - 1, start_time, time_limit)
            except TimeoutError:
                # Cofnij i rzuc wyjatek dalej
                game_board.set_empty(row, col)
                game_board.next_board = prev_next_board
                raise
            
            # Cofnij stan
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
            # Zapisz stan
            prev_next_board = game_board.next_board
            row, col = move
            game_board.make_move(row, col, player)
            
            try:
                eval_score, _ = minimax(game_board, player.opponent(), alpha, beta, depth - 1, start_time, time_limit)
            except TimeoutError:
                game_board.set_empty(row, col)
                game_board.next_board = prev_next_board
                raise

            # Cofnij stan
            game_board.set_empty(row, col)
            game_board.next_board = prev_next_board
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_best_move(game_board: UltimateBoard, player: Player) -> tuple[int, int]:
    start_time = time.time()
    time_limit = 0.095 # 95ms dla bezpieczenstwa (limit to zazwyczaj 100ms)
    best_move = None
    
    # Proste zabezpieczenie: pierwszy mozliwy ruch
    possible = game_board.possible_moves()
    if not possible:
        return 0, 0
    best_move = possible[0]
    
    # Poglebianie iteracyjne (Iterative Deepening)
    depth = 1
    max_depth = 10 # Sztywny limit
    
    try:
        while depth <= max_depth:
            _, move = minimax(game_board, player, -float("inf"), float("inf"), depth, start_time, time_limit)
            if move:
                best_move = move
            depth += 1
    except TimeoutError:
        pass # Zwroc najlepszy znaleziony do tej pory ruch
        
    return best_move

def game_loop() -> None:
    game_board: UltimateBoard = UltimateBoard()
    # Logika pierwszego ruchu: Jesli zaczynamy, gramy w srodek srodka
    first_turn = True
    
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
            first_turn = False
        
        # Hardcoded otwarcie dla X (jesli przeciwnik zaczyna -1 -1, to my ruszamy)
        if first_turn and opponent_row == -1:
             move = (4, 4)
             first_turn = False
        else:
             move = get_best_move(game_board, Player.PLAYER)
        
        if move:
            row, col = move
            game_board.make_move(row, col, Player.PLAYER)
            print(f"{row} {col}")
        else:
            print("0 0")

if __name__ == "__main__":
    game_loop()
