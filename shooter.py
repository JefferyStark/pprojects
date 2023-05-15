import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen configuration
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zombie Shooter")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Player
player_health = 100
player_speed = 10
player_radius = 20
player_pos = [width // 2, height // 2]

# Zombies
zombie_speed = 6
zombies = []

# Bullets
bullet_damage = 20
bullets = []

def spawn_zombie():
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left":
        x, y = 0, random.randint(0, height)
    elif side == "right":
        x, y = width, random.randint(0, height)
    elif side == "top":
        x, y = random.randint(0, width), 0
    else:
        x, y = random.randint(0, width), height

    size = random.randint(20, 50)
    health = random.randint(50, 500)
    zombie = {"pos": [x, y], "size": size, "health": health}
    zombies.append(zombie)

def move_toward(target, source, speed):
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    distance = (dx**2 + dy**2)**0.5
    if distance == 0:
        return source
    normalized_dx = dx / distance
    normalized_dy = dy / distance
    return [source[0] + normalized_dx * speed, source[1] + normalized_dy * speed]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_pos = player_pos[:]
            bullets.append(bullet_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed

    if random.random() < 0.01:
        spawn_zombie()

    for zombie in zombies:
        zombie["pos"] = move_toward(player_pos, zombie["pos"], zombie_speed)
        if ((player_pos[0] - zombie["pos"][0])**2 + (player_pos[1] - zombie["pos"][1])**2)**0.5 < player_radius + zombie["size"]:
            player_health -= 10
            if player_health <= 0:
                running = False

    for bullet in bullets[:]:
        bullet[0] += 20
        if bullet[0] > width:
            bullets.remove(bullet)
            continue
        for zombie in zombies[:]:
            if ((bullet[0] - zombie["pos"][0])**2 + (bullet[1] - zombie["pos"][1])**2)**0.5 < zombie["size"]:
                zombie["health"] -= bullet_damage
                bullets.remove(bullet)
                if zombie["health"] <= 0:
                    zombies.remove(zombie)
                break

    # Redraw screen
    screen.fill(WHITE)

    # Draw player
    pygame.draw.circle(screen, BLUE, (int(player_pos[0]), int(player_pos[1])), player_radius)

    # Draw zombies
    for zombie in zombies:
        pygame.draw.rect(screen, RED, pygame.Rect(zombie["pos"][0], zombie["pos"][1], zombie["size"], zombie["size"]))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, GREEN, (int(bullet[0]), int(bullet[1])), 5)

    # Draw health information
    health_text = font.render(f"Player Health: {player_health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()

