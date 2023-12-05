import pygame
from pygame.locals import *
from enum import Enum
from typing import List, Tuple


class GameState(Enum):
    ONGOING = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3


class ChessPiece:
    def __init__(self, piece_type: str, color: str):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = False

    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        raise NotImplementedError
        ("Subclasses must implement the is_valid_move method")


class Pawn(ChessPiece):
    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        direction = 1 if self.color == "white" else -1
        if not self.has_moved:
            return (
                (end_row - start_row) == direction
                or (end_row - start_row) == 2 * direction
            ) and start_col == end_col
        return (end_row - start_row) == direction and start_col == end_col


class Rook(ChessPiece):
    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        return start_row == end_row or start_col == end_col


class Knight(ChessPiece):
    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        return (
            abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1)
        or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)


class Bishop(ChessPiece):
    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        return abs(start_row - end_row) == abs(start_col - end_col)


class Queen(ChessPiece):
    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        return (
            start_row == end_row
            or start_col == end_col
            or abs(start_row - end_row) == abs(start_col - end_col)
        )


class King(ChessPiece):
    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    def can_castle(self, start_col: int, end_col: int) -> bool:
        return not self.has_moved and abs(end_col - start_col) == 2


class ChessBoard:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()

        self.board_size = 8
        self.square_size = self.width // self.board_size

        self.board = [
            [None for _ in range(self.board_size)]for _ in range
            (self.board_size)
        ]
        self.init_board()

        self.selected_piece = None
        self.game_state = GameState.ONGOING
        self.current_player = "white"

    def init_board(self):
        piece_order = ["R", "N", "B", "Q", "K", "B", "N", "R"]

        for col in range(self.board_size):
            self.board[1][col] = Pawn("P", "black")
            self.board[6][col] = Pawn("P", "white")

            self.board[0][col] = globals()[piece_order[col]]("B", "black")
            self.board[7][col] = globals()[piece_order[col]]("B", "white")

    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.square_size,
                        row * self.square_size,
                        self.square_size,
                        self.square_size,
                    ),
                )

    def draw_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if piece:
                    image = pygame.image.load(
                        f"images/{piece.color}_{piece.piece_type}.png"
                    )
                    image = pygame.transform.scale(
                        image, (self.square_size, self.square_size)
                    )
                    self.screen.blit(
                        image, (col * self.square_size, row * self.square_size)
                    )

    def draw_selected_piece_highlight(self):
        if self.selected_piece:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (
                    self.selected_piece[1] * self.square_size,
                    self.selected_piece[0] * self.square_size,
                    self.square_size,
                    self.square_size,
                ),
                5,
            )

    def draw_arrows(self, moves: List[Tuple[int, int]]):
        for move in moves:
            start_col, start_row = self.selected_piece[1],
            self.selected_piece[0]
            end_col, end_row = move[1], move[0]
            arrow_color = (
                255, 0, 0) if self.board[end_row][end_col] else (
                0, 255, 0)

            pygame.draw.line(
                self.screen,
                arrow_color,
                (
                    start_col * self.square_size + self.square_size // 2,
                    start_row * self.square_size + self.square_size // 2,
                ),
                (
                    end_col * self.square_size + self.square_size // 2,
                    end_row * self.square_size + self.square_size // 2,
                ),
                5,
            )

    def get_moves_for_selected_piece(self):
        row, col = self.selected_piece
        piece = self.board[row][col]

        if not piece or piece.color != self.current_player:
            return []

        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.is_valid_move(row, col, i, j):
                    moves.append((i, j))
        return moves

    def is_valid_move(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> bool:
        piece = self.board[start_row][start_col]
        if not piece:
            return False

        if piece.color != self.current_player:
            return False

        return piece.is_valid_move(start_row, start_col, end_row, end_col)

    def is_in_check(self, color: str) -> bool:
        # Placeholder: Implement checking if the specified color is in check
        return False

    def is_checkmate(self, color: str) -> bool:
        # Placeholder: Implement checking if the specified color is in
        # checkmate
        return False

    def switch_player(self):
        self.current_player = "white"
        if self.current_player == "black" else "black"

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_row, clicked_col = (
                        mouse_y // self.square_size,
                        mouse_x // self.square_size,
                    )

                    if self.selected_piece is None:
                        if (
                            self.board[clicked_row][clicked_col]
                            and self.board[clicked_row][clicked_col].color
                            == self.current_player
                        ):
                            self.selected_piece = (clicked_row, clicked_col)
                    else:
                        if (
                            clicked_row,
                            clicked_col,
                        ) in self.get_moves_for_selected_piece():
                            self.board[clicked_row][clicked_col] = self.board[
                                self.selected_piece[0]
                            ][self.selected_piece[1]]
                            self.board[self.selected_piece[0]][
                                self.selected_piece[1]
                            ] = None
                            self.selected_piece = None

                            if isinstance(
                                    self.board[clicked_row]
                                    [clicked_col], King):
                                self.game_state = (
                                    GameState.CHECKMATE
                                    if self.is_checkmate(self.current_player)
                                    else GameState.CHECK
                                )

                            self.switch_player()

            self.screen.fill((255, 255, 255))
            self.draw_board()
            self.draw_pieces()
            self.draw_selected_piece_highlight()

            if self.selected_piece:
                self.draw_arrows(self.get_moves_for_selected_piece())

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    chess_board = ChessBoard()
    chess_board.play()
