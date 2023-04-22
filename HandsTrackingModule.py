import cv2
import mediapipe as mp
import time
import math


class HandDetector:
    def __init__(self, mode=False, max_hands=2, model_ic=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.modelIc = model_ic
        self.detectionCon = detection_con
        self.trackCon = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelIc, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_positions(self, img, handno=0, draw=True):
        landmarks_list = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                height,width,channels = img.shape
                center_x, center_y = int(lm.x * width), int(lm.y * height)
                landmarks_list.append([id,center_x,center_y])
                if draw:
                    cv2.circle(img, (center_x,center_y),3,(0,0,0),cv2.FILLED)

        return landmarks_list
    
    def find_distance(self, p1, p2, img, draw=True):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1 - Index of Landmark 1.
        :param p2: Point2 - Index of Landmark 2.
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                    Image with output drawn
                    Line information
        """

        if self.results.multi_hand_landmarks:
            x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
            x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if draw:
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]




def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        sucess, img = cap.read()
        img = detector.find_hands(img)
        landmarks_list = detector.find_positions(img)


        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime

        cv2.putText(img,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)

        cv2.imshow('images', img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
