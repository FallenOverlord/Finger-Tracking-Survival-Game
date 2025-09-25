import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon = 0.5, trackCon= 0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        #static_image_model(false), numof hands:2, confidance:0.5, defalt params
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #extract hand pic
        #make sure there is something in the result
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:                        
                    #draw points of the hands using the media pipe
                    #for a single hand, hand 0(points, connections)
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)


        return img
    def findPosition(self, img, handNo, draw = True):
        lmList = []
                #extract hand pic
        #make sure there is something in the result
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
     
            #look for the id number and the landmark info in the extracted data
            #each id has a cooresponding landmark(eanch land mark has x, y and z; desmial, the ratial of the image)
            for id, lm in enumerate(myHand.landmark):

                #look for the height , width of the image
                h, w, c  = img.shape 
                cx, cy = int(lm.x * w), int (lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    #draw a larger(25) purple(255,0,255) circle on the screen(img)
                    cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
        return lmList

def main():
    #framrate
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        #get image from camera
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[8])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        #display the fps info on the screen
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        #show image box, name = img
        cv2.imshow("img", img)
        cv2. waitKey(1)

if __name__ == "__main__":
    main()
