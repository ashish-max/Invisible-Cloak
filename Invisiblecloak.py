import cv2
import numpy as np
import time

video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
time.sleep(3)

##Taking loop for video validation(capturing background)
for i in range (60):
    check,background = video.read()
    background = np.flip(background,axis = 1)

while(video.isOpened()):
    check,img = video.read()
    if check==False:
        break
    img = np.flip(img,axis = 1) ##we are using red cloth hence detecting them
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)##Red color from top of color pallete
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)##Red color from bottom of color pallete
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))##Morphing is used to avoid noise of recorded video
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))## red part in vdo-white
    mask2 = cv2.bitwise_not(mask1)##forming mask2 oppo to mask1,Red part in vdo-black
    res1 = cv2.bitwise_and(img,img, mask = mask2)##Red part in vdo-black,rest shows realtime video images
    res2 = cv2.bitwise_and(background,background, mask = mask1)##Red part in vdo shows real video,rest=black /oppo to res1
    ##blending res1&2
    final = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("final",final)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


    
    
    
