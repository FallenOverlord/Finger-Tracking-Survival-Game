import cv2
import mediapipe as mp
import time, os
#import hand tracking moduel
import htm
import pygame, sys, random

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
WIDTH = 950
HEIGHT = 750

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
BLUE = 0, 0, 255

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
ENEMY_WIDTH = 20
ENEMY_HEIGHT = 20

#font
pygame.font.init()
font = pygame.font.SysFont('Roman', 28)
font_large = pygame.font.SysFont('Roman', 32)
font_title = pygame.font.SysFont('Roman', 48)

# Screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand-Tracking Survival Game")
clock = pygame.time.Clock()

#sound
pygame.mixer.init()
# You may need to adjust the path or comment out if file doesn't exist
# SCREAM = pygame.mixer.Sound(os.path.join('pygame','duel', 'Assets', 'bo_strike.wav'))

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

def draw_button(screen, text, x, y, width, height, color, text_color):
    """Draw a button and return its rect for collision detection"""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    return button_rect

def show_start_screen(screen):
    """Display the start screen"""
    screen.fill(WHITE)
    
    # Title
    title_text = font_title.render("Hand-Tracking Survival Game", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    # Instructions
    instructions = [
        "Use your index finger to control the player",
        "Avoid the shapes and the chaser",
        "Survive as long as possible!",
        "",
        "Make sure your webcam is working"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50 + i*30))
        screen.blit(text, text_rect)
    
    # Start button
    start_button = draw_button(screen, "START GAME", WIDTH//2 - 100, HEIGHT*3//4, 200, 50, GREEN, WHITE)
    
    pygame.display.flip()
    return start_button

def show_game_over_screen(screen, elapsed_time):
    """Display the game over screen"""
    screen.fill(WHITE)
    
    # Game Over title
    game_over_text = font_title.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(game_over_text, game_over_rect)
    
    # Survival time
    time_text = font_large.render(f"You survived {elapsed_time} seconds!", True, BLACK)
    time_rect = time_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(time_text, time_rect)
    
    # Buttons
    restart_button = draw_button(screen, "PLAY AGAIN", WIDTH//2 - 220, HEIGHT*3//4, 200, 50, GREEN, WHITE)
    quit_button = draw_button(screen, "QUIT", WIDTH//2 + 20, HEIGHT*3//4, 200, 50, RED, WHITE)
    
    pygame.display.flip()
    return restart_button, quit_button

def reset_game():
    """Reset all game variables to initial state"""
    player_x = WIDTH / 2
    player_y = HEIGHT / 2
    chaser_x = WIDTH / 4
    chaser_y = HEIGHT / 4
    chaser_radius = 25
    chaser_speed = 3
    shapes = []
    start_time = pygame.time.get_ticks()
    
    return player_x, player_y, chaser_x, chaser_y, chaser_radius, chaser_speed, shapes, start_time

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

def main():
    #use integrated cam
    cap = cv2.VideoCapture(0)
    #use "handDetector function" in handDetector moduel
    detector = htm.handDetector()
    
    # Game state
    game_state = MENU
    
    # Initialize game variables
    player_x, player_y, chaser_x, chaser_y, chaser_radius, chaser_speed, shapes, start_time = reset_game()
    player_size = 30
    fps = 80
    elapsed_time = 0
    
    running = True
    while running:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if game_state == MENU:
                    start_button = show_start_screen(screen)
                    if start_button.collidepoint(mouse_pos):
                        game_state = PLAYING
                        player_x, player_y, chaser_x, chaser_y, chaser_radius, chaser_speed, shapes, start_time = reset_game()
                
                elif game_state == GAME_OVER:
                    restart_button, quit_button = show_game_over_screen(screen, elapsed_time)
                    if restart_button.collidepoint(mouse_pos):
                        game_state = PLAYING
                        player_x, player_y, chaser_x, chaser_y, chaser_radius, chaser_speed, shapes, start_time = reset_game()
                    elif quit_button.collidepoint(mouse_pos):
                        running = False
        
        if game_state == MENU:
            show_start_screen(screen)
        
        elif game_state == PLAYING:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
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
            if success:
                img = detector.findHands(img)
                #land marks analysis the critical points on the picture
                lmList = detector.findPosition(img)
                if len(lmList) != 0:
                    #c.p. 8 is second finger
                    player_x = WIDTH - lmList[8][1]
                    player_y = lmList[8][2]

                #display the fps info on the camera screen
                cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                cv2.imshow("Hand Tracking", img)
                cv2.waitKey(1)

            # Chaser AI
            if chaser_x < player_x:
                chaser_x += chaser_speed
            elif chaser_x > player_x:
                chaser_x -= chaser_speed

            if chaser_y < player_y:
                chaser_y += chaser_speed
            elif chaser_y > player_y:
                chaser_y -= chaser_speed

            # Clear screen
            screen.fill(WHITE)
            
            # Display survival time
            time_text = font.render(f"Survived Time: {elapsed_time} seconds", True, BLACK)
            screen.blit(time_text, (10, 10))

            # Draw player (only if hand is detected)
            if len(lmList) != 0:
                pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
            
            # Draw chaser
            pygame.draw.circle(screen, chaser_color, (int(chaser_x), int(chaser_y)), int(chaser_radius))

            # Generate new shapes
            if random.random() < 0.02:  # 2% chance to generate a shape each frame
                shape_type = random.choice(["rectangle", "circle", "triangle"])
                size = random.randint(40, 90)
                (x, y), (speedx, speedy) = random_edge_position_and_velocity(size)
                shapes.append([x, y, size, speedx, speedy, shape_type])
            
            # Update and draw shapes
            for shape in shapes[:]:
                if shape[5] == "rectangle":
                    pygame.draw.rect(screen, RED, (shape[0], shape[1], shape[2], shape[2]))
                elif shape[5] == "circle":
                    pygame.draw.circle(screen, GREEN, (int(shape[0]+shape[2]/2), int(shape[1]+shape[2]/2)), int(shape[2]/2))
                elif shape[5] == "triangle":
                    pygame.draw.polygon(screen, PURPLE, [(shape[0], shape[1] + shape[2]), 
                                                        (shape[0] + shape[2]/2, shape[1]), 
                                                        (shape[0] + shape[2], shape[1] + shape[2])])
                
                shape[0] += shape[3]
                shape[1] += shape[4]

                # Remove shapes that go off screen
                if shape[0] <= -shape[2] or shape[0] >= WIDTH or shape[1] <= -shape[2] or shape[1] >= HEIGHT:
                    shapes.remove(shape)
                    continue

                # Collision detection with shapes (only if hand is detected)
                if len(lmList) != 0:
                    if (player_x < shape[0] + shape[2] and player_x + player_size > shape[0] and
                        player_y < shape[1] + shape[2] and player_y + player_size > shape[1]):
                        
                        print("Collision detected! Survived", elapsed_time, "seconds")
                        # SCREAM.play()  # Uncomment if you have the sound file
                        game_state = GAME_OVER
                        break

            # Collision detection with chaser (only if hand is detected)
            if len(lmList) != 0:
                dist = ((chaser_x - (player_x + player_size / 2))**2 + (chaser_y - (player_y + player_size / 2))**2)**0.5
                if dist < (player_size / 2 + chaser_radius):
                    print("Caught by the chaser! Survived", elapsed_time, "seconds")
                    # SCREAM.play()  # Uncomment if you have the sound file
                    game_state = GAME_OVER

            pygame.display.flip()
        
        elif game_state == GAME_OVER:
            show_game_over_screen(screen, elapsed_time)

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()