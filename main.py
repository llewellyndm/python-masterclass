import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60 # max fps if computer can handle it
PLAYER_SPEED = 5
BACKGROUND_SCROLL_SPEED = 2

# Create a Pygame window and set its dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Space Attack")

# Clock
clock = pygame.time.Clock()

# Background
# building path manually instead of hardcoding here for cross-platform support
background = pygame.image.load(os.path.join("assets", "images", "space_bg.png")).convert()

# Going to loop between two backgrounds to create infinite scrolling effect
background_rect_one = background.get_rect()
background_rect_one.x = 0
background_rect_two = background.get_rect()
background_rect_two.x = WIDTH

# Player
player = pygame.image.load(os.path.join("assets", "images", "spaceship_pl.png")).convert_alpha() # more performant if converted
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

    # Background scrolling
    if background_rect_one.x < -800:
        background_rect_one.x = WIDTH
    if background_rect_two.x < -800:
        background_rect_two.x = WIDTH

    background_rect_one.x -= BACKGROUND_SCROLL_SPEED
    background_rect_two.x -= BACKGROUND_SCROLL_SPEED

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += PLAYER_SPEED


    # Draw surfaces 
    # screen.fill("#4c43ea") # if you want to fill with single colour
    # draws the following in order i.e. bgs first, then player
    screen.blit(background, background_rect_one)
    screen.blit(background, background_rect_two)
    screen.blit(player, player_rect)

    # Update display
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()