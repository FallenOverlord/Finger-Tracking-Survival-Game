import cv2
import mediapipe as mp
import time, os
#import hand tracking moduel
import htm
import pygame, sys, random

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
#framrate
#use integrated cam
cap = cv2.VideoCapture(0)
#use "handDetector function" in handDetector moduel
detector = htm.handDetector()
# Screen dimensions
WIDTH = 950
HEIGHT = 750
#game consts
#colors collection in RGB
PINK = 220, 105, 225    
BLACK = 0, 0, 0 
RED = 255, 0, 0 
GREEN = 0, 238, 0
WHITE = 255, 255, 255
BLOOD = 220, 0, 0
PURPLE = 153, 51, 255
GOLD = 255, 255, 0
ORANGE = 255, 165, 0

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
ENEMY_WIDTH = 20
ENEMY_HEIGHT = 20

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#font
pygame.font.init()
font = pygame.font.SysFont('Roman', 28)
font_large = pygame.font.SysFont('Roman', 32)

# Screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Shapes!")
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

#sound
pygame.mixer.init()
SCREAM = pygame.mixer.Sound(os.path.join('pygame','duel', 'Assets', 'bo_strike.wav'))

# Define the player
player_size = 30
player_x = WIDTH / 2
player_y = HEIGHT / 2
chaser_x = WIDTH / 4
chaser_y = HEIGHT / 4
chaser_radius = 25
chaser_speed = 3  # This can be adjusted based on desired difficulty

#setup pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps = 80
timer = pygame.time.Clock()

#list of objects on the screen
shapes = []

def random_edge_position_and_velocity(size):
    edge = random.choice(["top", "bottom", "left", "right"])
    base_speed = random.randint(2, 4)  # Base speed

    # Randomly negate base_speed for variability in direction
    speed_variety = [-base_speed, base_speed]
    if edge == "top":
        return (random.randint(0, WIDTH - size), -size), (random.choice(speed_variety), random.randint(1, base_speed))
    elif edge == "bottom":
        return (random.randint(0, WIDTH - size), HEIGHT), (random.choice(speed_variety), -random.randint(1, base_speed))
    elif edge == "left":
        return (-size, random.randint(0, HEIGHT - size)), (random.randint(1, base_speed), random.choice(speed_variety))
    else:  # "right"
        return (WIDTH, random.randint(0, HEIGHT - size)), (-random.randint(1, base_speed), random.choice(speed_variety))


# Main loop
running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert milliseconds to seconds
    chaser_speed = 3 + elapsed_time/8
    chaser_radius = 25 + elapsed_time
    if elapsed_time <= 10:
        chaser_color = GREEN
    elif elapsed_time <= 20:
        chaser_color = BLUE
    else:
        chaser_color = BLOOD

    #get image from camera
    success, img = cap.read()
    img = detector.findHands(img)
    #land marks analysis the critical points on the picture
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        #print(lmList[8][1], lmList[8][2])
        #c.p. 8 is second fingure
        player_x = WIDTH - lmList[8][1]
        player_y = lmList[8][2]

    # This should be placed inside the main loop, before the shape handling logic
    if chaser_x < player_x:
        chaser_x += chaser_speed
    elif chaser_x > player_x:
        chaser_x -= chaser_speed

    if chaser_y < player_y:
        chaser_y += chaser_speed
    elif chaser_y > player_y:
        chaser_y -= chaser_speed

    #display the fps info on the screen
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    #show image box, name = img
    cv2.imshow("img", img)
    cv2. waitKey(1)

    screen.fill(WHITE)
    time_text = font.render(f"Survived Time: {elapsed_time} seconds", True, (0, 0, 0))  # Render the text in black color
    screen.blit(time_text, (10, 10))  # Draw the text at position (10, 10)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if lmList != 0:
        player = pygame.draw.rect(screen, GREEN, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
    
    pygame.draw.circle(screen, chaser_color, (int(chaser_x), int(chaser_y)), chaser_radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            pygame.quit()
            sys.exit()


    if random.random() < 0.02:  # 2% chance to generate a shape each frame
        shape_type = random.choice(["rectangle", "circle", "triangle"])
        size = random.randint(40, 90)
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
            print("Collision detected!", "survived", elapsed_time, "seconds")
        dist = ((chaser_x - (player_x + player_size / 2))**2 + (chaser_y - (player_y + player_size / 2))**2)**0.5
        if dist < (player_size / 2 + chaser_radius):
            
            running = False
            
            print("Caught by the chaser!", "survived", elapsed_time, "seconds")

    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    pygame.display.flip()

    clock.tick(fps)

SCREAM.play()
pygame.quit()
