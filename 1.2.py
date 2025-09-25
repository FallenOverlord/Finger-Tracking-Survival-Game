import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Shapes!")
clock = pygame.time.Clock()

# Define the player
player_size = 50
player_x = WIDTH / 2
player_y = HEIGHT / 2
player_speed = 5

shapes = []

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if random.random() < 0.02:  # 2% chance to generate a shape each frame
        size = random.randint(20, 50)
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        speedx = random.randint(-3, 3)
        speedy = random.randint(-3, 3)
        shapes.append([x, y, size, speedx, speedy])

    for shape in shapes[:]:
        pygame.draw.rect(screen, RED, (shape[0], shape[1], shape[2], shape[2]))
        shape[0] += shape[3]
        shape[1] += shape[4]

        # Shape boundary
        if shape[0] <= 0 or shape[0] + shape[2] >= WIDTH:
            shapes.remove(shape)
        if shape[1] <= 0 or shape[1] + shape[2] >= HEIGHT:
            shapes.remove(shape)

        # Collision detection
        if (player_x < shape[0] + shape[2] and player_x + player_size > shape[0] and
            player_y < shape[1] + shape[2] and player_y + player_size > shape[1]):
            running = False
            print("Collision detected!")

    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    pygame.display.flip()

    clock.tick(30)

pygame.quit()

