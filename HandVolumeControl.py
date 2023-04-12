import cv2
import time
import numpy as np
import math
import HandsTrackingModule as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#################################################
cam_width, cam_height = 640,480
pTime = 0
#################################################


cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

detector = htm.HandDetector(detection_con=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol =volRange[0]
maxVol =volRange[1]

vol = 0
volPer = 0
volBar = 400

while True:
    _, img = cap.read()
    img = detector.find_hands(img)
    landmark_list = detector.find_positions(img, draw=False)
    # print(landmark_list)

    if landmark_list:
        x1,y1 = landmark_list[4][1], landmark_list[4][2]
        x2,y2 = landmark_list[8][1], landmark_list[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2,y2),10,(255,0,0),cv2.FILLED)
        cv2.circle(img, (cx,cy),10,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

        line_length = math.hypot(x2-x1, y2-y1)
        print(line_length)

        vol = np.interp(line_length, [30,200],[minVol, maxVol])
        volBar = np.interp(line_length, [30,200],[400,150])
        volPer = np.interp(line_length, [30,200],[0,100])
        
        volume.SetMasterVolumeLevel(vol, None)

        if line_length<=50:
            cv2.circle(img, (cx,cy),10,(0,255,0),cv2.FILLED)

    cv2.rectangle(img, (50,150),(85,400),(255,0,0),2)
    cv2.rectangle(img, (50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (50,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            

    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, f'FPS:{fps}', (40,50),cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,255),1)

    cv2.imshow('output',img)
    cv2.waitKey(1)