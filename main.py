import pygame
from chessboard.chessboard import ChessBoard
from pieces.piece import ChessPiece


def main():
    pygame.init()

    chess_game = ChessBoard()

    # Example: Create pieces and place them on the chessboard
    white_pawn = ChessPiece("pawn", "white")
    black_knight = ChessPiece("knight", "black")

    chess_game.place_piece(1, 2, white_pawn)
    chess_game.place_piece(6, 3, black_knight)

    chess_game.run_game()

    pygame.quit()


if __name__ == "__main__":
    main()
