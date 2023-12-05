from chessboard.chessboard import ChessBoard
from pieces.piece import ChessPiece


def main():
    # Create an instance of the ChessBoard
    chess_game = ChessBoard()

    # Example: Create a pawn and place it on the chessboard
    pawn = ChessPiece("pawn", "white")
    chess_game.place_piece(1, 2, pawn)

    # Run the game loop
    chess_game.run_game()


if __name__ == "__main__":
    main()
