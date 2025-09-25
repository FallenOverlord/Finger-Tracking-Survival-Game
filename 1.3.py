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
GREEN = (0, 255, 0)

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

def random_edge_position_and_velocity(size):
    edge = random.choice(["top", "bottom", "left", "right"])
    if edge == "top":
        return (random.randint(0, WIDTH - size), -size), (random.randint(-2, 2), random.randint(1, 3))
    elif edge == "bottom":
        return (random.randint(0, WIDTH - size), HEIGHT), (random.randint(-2, 2), random.randint(-3, -1))
    elif edge == "left":
        return (-size, random.randint(0, HEIGHT - size)), (random.randint(1, 3), random.randint(-2, 2))
    else:  # "right"
        return (WIDTH, random.randint(0, HEIGHT - size)), (random.randint(-3, -1), random.randint(-2, 2))


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
        shape_type = random.choice(["rectangle", "circle", "triangle"])
        size = random.randint(20, 50)
        (x, y), (speedx, speedy) = random_edge_position_and_velocity(size)
        shapes.append([x, y, size, speedx, speedy, shape_type])
    for shape in shapes[:]:
        if shape[5] == "rectangle":
            pygame.draw.rect(screen, RED, (shape[0], shape[1], shape[2], shape[2]))
        elif shape[5] == "circle":
            pygame.draw.circle(screen, GREEN, (int(shape[0]+shape[2]/2), int(shape[1]+shape[2]/2)), int(shape[2]/2))
        elif shape[5] == "triangle":
            pygame.draw.polygon(screen, BLUE, [(shape[0], shape[1] + shape[2]), 
                                                (shape[0] + shape[2]/2, shape[1]), 
                                                (shape[0] + shape[2], shape[1] + shape[2])])
        
        shape[0] += shape[3]
        shape[1] += shape[4]

        # Shape boundary
        if shape[0] <= -shape[2] or shape[0] >= WIDTH or shape[1] <= -shape[2] or shape[1] >= HEIGHT:
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
