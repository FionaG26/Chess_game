import pygame


class ChessBoard:
    def __init__(self):
        self.board_size = 8
        self.square_size = 50
        self.total_size = self.square_size * self.board_size

        # Colors
        self.white = (255, 255, 255)
        self.black = (89, 89, 89)

        # Create Pygame window
        self.screen = pygame.display.set_mode(
            (self.total_size, self.total_size)
        )
        pygame.display.set_caption("3D Chess Board")

        self.clock = pygame.time.Clock()

        # Placeholder graphics for chess pieces
        self.piece_images = {
            'pawn': pygame.Surface((self.square_size, self.square_size)),
            'rook': pygame.Surface((self.square_size, self.square_size)),
            'knight': pygame.Surface((self.square_size, self.square_size)),
            'bishop': pygame.Surface((self.square_size, self.square_size)),
            'queen': pygame.Surface((self.square_size, self.square_size)),
            'king': pygame.Surface((self.square_size, self.square_size)),
        }

        # Set placeholder colors for pieces
        for piece_surface in self.piece_images.values():
            piece_surface.fill((255, 0, 0))  # Placeholder: Red color

        # Initial piece positions (row, column)
        self.piece_positions = {
            'pawn': [(1, i) for i in range(self.board_size)],
            'rook': [(0, 0), (0, 7)],
            'knight': [(0, 1), (0, 6)],
            'bishop': [(0, 2), (0, 5)],
            'queen': [(0, 3)],
            'king': [(0, 4)],
        }

    def draw_chessboard(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.white if (row + col) % 2 == 0 else self.black
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.square_size,
                        row * self.square_size,
                        self.square_size,
                        self.square_size
                    )
                )

    def draw_pieces(self):
        for piece_type, positions in self.piece_positions.items():
            for position in positions:
                row, col = position
                x = col * self.square_size
                y = row * self.square_size

                piece_image = self.piece_images[piece_type]
                self.screen.blit(piece_image, (x, y))

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((255, 255, 255))  # Fill background with white
            self.draw_chessboard()
            self.draw_pieces()

            pygame.display.flip()
            self.clock.tick(60)
