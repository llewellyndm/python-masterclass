import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600

# Create a Pygame window and set its dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Space Attack")

# Get background image
# building path manually instead of hardcoding here for cross-platform support
background = pygame.image.load(os.path.join("assets", "images", "space_bg.png"))

# Player
player = pygame.image.load(os.path.join("assets", "images", "spaceship_pl.png"))
player_rect = player.get_rect()
player_rect.midleft = (25, HEIGHT // 2) # double slash for integer division

# Main game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic 

    # Draw surfaces 
    # screen.fill("#4c43ea") # if you want to fill with single colour
    # draws the following in order i.e. bg first, then player
    screen.blit(background, (0, 0))
    screen.blit(player, player_rect)

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()

