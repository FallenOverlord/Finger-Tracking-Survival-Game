import cv2
import mediapipe as mp
import time
import htm
import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()
#framrate

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

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


SCREEN_WIDTH = 450
SCREEN_HEIGHT = 300
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15
ENEMY_WIDTH = 20
ENEMY_HEIGHT = 20

#font
pygame.font.init()
font = pygame.font.SysFont('Roman', 28)
font_large = pygame.font.SysFont('Roman', 32)
#gravity
g = 1

#jump height
y_change = 0

#speed
x_change = 0

#game variables
score = 0
player_x = 100
player_y = 200

player_vel = 3

enemy_vel = 2
enemy_y= 200
enemy_x = [200, 400, 600]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("v1.1")
background = BLACK
fps = 60
timer = pygame.time.Clock()
active = 0

score = 0
triggered = False

while True:

    #get image from camera
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        #print(lmList[8][1], lmList[8][2])
        player_x = SCREEN_WIDTH - lmList[8][1]
        player_y = lmList[8][2]


    #display the fps info on the screen
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    #show image box, name = img
    cv2.imshow("img", img)
    cv2. waitKey(1)



    screen.fill(background)



    if lmList != 0:
        player = pygame.draw.rect(screen, GREEN, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(score)
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(fps)



