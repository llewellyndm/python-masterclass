import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60 # max fps if computer can handle it
PLAYER_SPEED = 5
BACKGROUND_SCROLL_SPEED = 2
WHITE = (255, 255, 255)
BULLET_SPEED = 5

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


def load_image(filename):
    # convert to alpha as more performant
    return pygame.image.load(os.path.join("assets", "images", f"{filename}.png")).convert_alpha()


# Player
player = load_image("spaceship_pl")
player_rect = player.get_rect()
player_rect.midleft = (25, HEIGHT // 2) # double slash for integer division

# Enemies
enemy_one = load_image("spaceship_en_one")
enemy_two = load_image("spaceship_en_two")
enemy_three = load_image("spaceship_en_three")
enemy_four = load_image("spaceship_en_four")
enemy_five = load_image("spaceship_en_five")
enemy_images = [enemy_one, enemy_two, enemy_three, enemy_four, enemy_five]
enemy_speed = 5
enemy_spawn_rate = 3000
last_enemy_spawn = 0
enemies = []

# Bullets
bullet = load_image("bullet")
bullet_cooldown = 800
last_bullet_time = 0
bullets = []

def load_font(font_size):
    return pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), font_size)

# Score
spaceship = load_image("spaceship")
spaceship_rect = spaceship.get_rect()
spaceship_rect.topleft = (25, 25)
score_font = load_font(32)
score = 0

# Title screen
title_font = load_font(72)
instruction_font = load_font(32)
title_string = "SPACE ATTACK!"
instruction_string = "Press ENTER to start"
title_text = title_font.render(title_string, True, WHITE) # middle param for anti-aliasing
instruction_text = instruction_font.render(instruction_string, True, WHITE)
title_text_rect = title_text.get_rect()
title_text_rect.center = (WIDTH // 2, 120)
instruction_text_rect = instruction_text.get_rect()
instruction_text_rect.center = (WIDTH // 2, 480)
title_image = player
title_image_rect = title_image.get_rect()
title_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# Main game loop
game_over = True
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Game logic
        current_time = pygame.time.get_ticks()

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
        
        # Shoot bullets
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_cooldown:
            bullet_image = bullet
            bullet_rect = bullet_image.get_rect()
            bullet_rect.center = player_rect.center
            bullets.append((bullet_image, bullet_rect))
            last_bullet_time = current_time

        # Bullet movement
        for bullet_image, bullet_rect in bullets:
            bullet_rect.x += 5
        bullets = [(bullet_image, bullet_rect) for bullet_image, bullet_rect in bullets if bullet_rect.left < WIDTH]

        # Enemy movement
        for enemy_image, enemy_rect in enemies:
            enemy_rect.x -= enemy_speed
        # then get rid of enemies that have left screen to avoid memory issues
        enemies = [(enemy_image, enemy_rect) for enemy_image, enemy_rect in enemies if enemy_rect.right > 0]
        
        # Collision detection
        for enemy_image, enemy_rect in enemies:
            if enemy_rect.colliderect(player_rect):
                game_over = True
            for bullet_image, bullet_rect in bullets:
                if enemy_rect.colliderect(bullet_rect):
                    score += 1
                    enemies.remove((enemy_image, enemy_rect))
                    bullets.remove((bullet_image, bullet_rect))

        # Update score
        score_text = score_font.render(f"{score}", True, WHITE)
        
        # Enemy spawning
        if current_time - last_enemy_spawn > enemy_spawn_rate:
            enemy_image = random.choice(enemy_images)
            enemy_rect = enemy_image.get_rect()
            enemy_rect.x = (WIDTH + enemy_rect.width)
            lane = random.randint(1, 3)
            if lane == 1:
                enemy_rect.y = 0
            elif lane == 2:
                enemy_rect.y = (HEIGHT // 2) - (enemy_rect.height // 2)
            else:
                enemy_rect.y = HEIGHT - enemy_rect.height
            enemies.append((enemy_image, enemy_rect))
            last_enemy_spawn = current_time


        # Draw surfaces 

        # screen.fill("#4c43ea") # if you want to fill with single colour
        # draws the following in order i.e. bgs first, then player
        screen.blit(background, background_rect_one)
        screen.blit(background, background_rect_two)
        screen.blit(player, player_rect)
        for enemy_image, enemy_rect in enemies:
            screen.blit(enemy_image, enemy_rect)
        for bullet_image, bullet_rect in bullets:
            screen.blit(bullet_image, bullet_rect)
        screen.blit(spaceship, spaceship_rect)
        screen.blit(score_text, (80, 40))
        
            
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            player_rect.midleft = (25, HEIGHT // 2)
        enemies.clear()
        bullets.clear()
        score = 0
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_text_rect)
        screen.blit(instruction_text, instruction_text_rect)
        screen.blit(title_image, title_image_rect)

    # Update display
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()