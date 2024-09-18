import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600

# Create a Pygame window and set its dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Space Attack")

# Main game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic 

    # Draw surfaces 
    screen.fill("red")

    # Update dispay
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()

