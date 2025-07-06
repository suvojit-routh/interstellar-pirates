import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)

# Player setup
player = pygame.Rect(100, 100, 40, 40)
speed = 5

font = pygame.font.SysFont(None, 48)
timer = 60  # seconds
start_ticks = pygame.time.get_ticks()

while True:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Timer
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, timer - seconds)
    timer_surf = font.render(f"Time: {time_left}", True, RED)
    screen.blit(timer_surf, (600, 20))

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[K_w]: player.move_ip(0, -speed)
    if keys[K_s]: player.move_ip(0, speed)
    if keys[K_a]: player.move_ip(-speed, 0)
    if keys[K_d]: player.move_ip(speed, 0)

    pygame.draw.rect(screen, (0, 0, 255), player)

    # Game over
    if time_left <= 0:
        game_over = font.render("You Died!", True, RED)
        screen.blit(game_over, (300, 250))

    pygame.display.flip()
    clock.tick(60)
