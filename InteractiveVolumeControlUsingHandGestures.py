import numpy as np
import cv2
import time 
import mediapipe as mp
import math
import os



from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTracking30FPSUsingOpenCV as htm

wCam,hCam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
detector=htm.HandDetector(detectionCon=0.7)
#devices volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
vol =0
volBar=400
volPer=0


while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList, _ =detector.findPosition(img,results=True,draw=True)
    if len(lmList) >=9:
        # print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(0,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(0,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100])
        print(int(length),vol)



        if length <50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
            cv2.rectangle(img,f'{int(volPer)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)

    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
    cv2.imshow('Image',img)
    key=cv2.waitKey(10)
    if key==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    
