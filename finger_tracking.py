import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
#static_image_model(false), numof hands:2, confidance:0.5, defalt params
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

#framrate
pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    #extract hand pic
    #make sure there is something in the result
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #draw points of the hands using the media pipe
            #for a single hand, hand 0(points, connections)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            #look for the id number and the landmark info in the extracted data
            #each id has a cooresponding landmark(eanch land mark has x, y and z; desmial, the ratial of the image)
            for id, lm in enumerate(handLms.landmark):

                #look for the height , width of the image
                h, w, c  = img.shape
                cx, cy = int(lm.x * w), int (lm.y * h)
                print("id:", id," cx:", cx," cy:", cy)

                #if id 0 is detected
                if id == 8:
                    #draw a larger(25) purple(255,0,255) circle on the screen(img)
                    cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)



    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    #display the fps info on the screen
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    #show image box, name = img
    cv2.imshow("img", img)
    cv2. waitKey(1)

