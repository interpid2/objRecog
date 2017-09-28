import cv2
import numpy as np

def loadBackground():
    _,background=cap.read()
    background=cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)    
    return background

def drawRect():
    detObj=len(c)
    elements=np.zeros((1,5))
    #print 'Number of detected objects: ',detObj
    for i in range(detObj):
        area=cv2.minAreaRect(c[i])
        x=int(area[0][0])
        y=int(area[0][1])
        w=int(area[1][0]/2)
        h=int(area[1][1]/2)
        if w*h<75.:
            continue
        if w>h:
            temp=w
            w=h
            h=temp
        elements=np.vstack((elements,[x,480-y,h,w,90+np.round(area[2],5)]))
        cv2.drawMarker(o,(x,y),(0,0,255),cv2.MARKER_TILTED_CROSS,8,1)
        box=np.int0(cv2.boxPoints(area))
        cv2.drawContours(o,[box],0,(0,255,0),2)
        cv2.putText(o,'Obj'+str(i),(x+5,y+5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1)
    
def processImg():
    _,orig=cap.read()
    frame=orig.copy()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.GaussianBlur(frame,(15,15),7)
    diff=frame-background
    diff[diff<0]=0
    diff[diff>thrs]=0
    _,diff=cv2.threshold(diff,20,255,cv2.THRESH_BINARY)
    for x in range(5):
        diff=cv2.erode(diff,None)
    for x in range(5):
        diff=cv2.dilate(diff,None)
        
    img,cont,_=cv2.findContours(diff,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    subtractor.clear()
    return orig,diff,cont

cap=cv2.VideoCapture(0)
subtractor=cv2.createBackgroundSubtractorMOG2()
background=loadBackground()
thrs=230
while(True):
    try:
        o,d,c=processImg()
	drawRect()
        cv2.imshow('Detected edges',o)
        cv2.imshow('Frame differencing into binary',d)
        wK=cv2.waitKey(5)
        if wK==ord('\x1b'): #brake on escape key
            break
        if wK==ord('b'): #reload background on key 'b'
            background=loadBackground()
    except KeyboardInterrupt or Exception:
        print 'Exception caught. Releasing cap and destroying windows'
        cap.release()
        cv2.destroyAllWindows()
    