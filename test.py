import pygame

pygame.init()

# Create a Pygame window
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Test Window")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black color
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
