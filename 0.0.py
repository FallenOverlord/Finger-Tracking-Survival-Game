import cv2
import mediapipe as mp
import time
import htm
import pygame, sys

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
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20

FPS = 60

background = BLACK
player_x = 0
player_y = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:

    #get image from camera
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[8][1], lmList[8][2])
        player_x = lmList[8][1]
        player_y = lmList[8][2]

    #display the fps info on the screen
    cv2.putText(img, str(int(FPS)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    #show image box, name = img
    cv2.imshow("img", img)
    cv2. waitKey(1)



    screen.fill(background)
    if lmList != 0:
        player = pygame.draw.rect(screen, GREEN, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    clock.tick(FPS)



