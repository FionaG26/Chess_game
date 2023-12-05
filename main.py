from chessboard.chessboard import ChessBoard
from pieces.piece import ChessPiece

def main():
    # Create an instance of the ChessBoard
    chess_game = ChessBoard()

    # Example: Create a pawn and place it on the chessboard
    pawn = ChessPiece("pawn", "white")  # Replace with your actual ChessPiece class
    chess_game.place_piece(1, 2, pawn)  # Replace with your actual method for placing a piece

    # Run the game loop
    chess_game.run_game()

if __name__ == "__main__":
    main()
