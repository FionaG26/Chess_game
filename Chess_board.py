import pygame
import sys

# Initialize Pygame
pygame.init()

class ChessBoard:
    def __init__(self):
        self.board_size = 8
        self.square_size = 50
        self.total_size = self.square_size * self.board_size

        # Colors
        self.white = (255, 255, 255)
        self.black = (89, 89, 89)

        # Create Pygame window
        self.screen = pygame.display.set_mode((self.total_size, self.total_size))
        pygame.display.set_caption("3D Chess Board")

        self.clock = pygame.time.Clock()

        # Run the game loop
        self.run_game()

    def draw_chessboard(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.white if (row + col) % 2 == 0 else self.black

                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))  # Fill background with white
            self.draw_chessboard()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    ChessBoard().run_game()
