#Importing the libraries
import cv2
import numpy as np
import time
import math

#Video  capture object
video_capture = cv2.VideoCapture(0)
len1 = []

while(True):
    kernel = np.ones((3,3),np.uint8)                          #filtering kernel
    lower_bound_color = np.array([0,133,77],np.uint8)         #range for creating mask to seperate skin colour from video frame
    upper_bound_color = np.array([235,173,127],np.uint8)
    ret, frame = video_capture.read()
    
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)     #convertibg bgr image to YCR_CB format
    black = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)           #conversion to grayscale
    
    ret , threshold = cv2.threshold(black, 150, 255, cv2.THRESH_BINARY_INV)
    
    #using range created above to seperate of skin colour from frame
    filter_ = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)
    filter_ = cv2.erode(filter_,kernel,iterations = 1)
    comb = cv2.bitwise_or(filter_,threshold)
    
    #Drawing rectange to take input from frame (input region)
    cv2.rectangle(frame,(520,360),(635,470),(255,0,0),3)
    
   #seperating the input region
    img1 = comb[143:390,203:417]
    
    #eroding the mask to get clear and shaper mask
    img1 = cv2.erode(img1,kernel,iterations = 4)
  
    #cv2.imshow("img1",img1)
    
   #Finding contors of eroded mask image
    contours, hierarchy = cv2.findContours(img1.copy(), 
                                            cv2.RETR_TREE,
	                                        cv2.CHAIN_APPROX_SIMPLE)
  
    
    hull = frame
    cv2.rectangle(hull,(200,140),(420,392),(0,0,255),3)
    
    hull_li = []
    hull_li1 = []
    len1t = 0
    areat = 0
    peri = 0

    for cnt in contours:
  
        area = cv2.contourArea(cnt)
        if area > 1000:                      # eliminating small contors 
    
            len1t = len1t + cv2.arcLength(cnt,True)  #finding  the total length of contor
            areat = areat + cv2.contourArea(cnt)     #finding  the total area of contor
            epis = 0.02*cv2.arcLength(cnt,True)      # Approxing small defects
            
            approx = cv2.approxPolyDP(cnt,epis,True)
            hull= cv2.convexHull(approx,returnPoints = True) #Drawing hull around contor image
  
            #Finding the extreme points of contours
            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])     
            rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
            topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
            bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
            #a = (22,300)

           
            #cv2.drawContours(frame, [cnt], -1,(255,0,255) , 1)

            #Drawing contour on black image
            bl = np.zeros([frame.shape[0], frame.shape[1],3],'uint8')
            cv2.drawContours(bl, [hull],-1,255,2)
            
            
            temp = bl[0:247,0:214]
          
            # Finding number of lines in mask image use houghlines functions gray>canny>finding
            gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            cc = cv2.Canny(gray, 10, 150)
            lines = cv2.HoughLines(cc, rho = 1,theta = 1*np.pi/180,threshold = 100)
            

            #Finding the number of corners of hull with certain parameters like distance between to  consider  them as points
            corners = cv2.goodFeaturesToTrack(gray, 0, 0.2, 20) 
            corners = np.int0(corners)
            #Drawing a circle at corners
            for i in corners: 
                x, y = i.ravel() 
                cv2.circle(temp, (x, y), 4, (0,255,0), -1)

            #Finh minimum bounding rectangle for contour
            x,y,w,h = cv2.boundingRect(cnt)
            peri = peri + 2*(w+h)

            #Combining hull with image
            temp1 = frame[143:390,203:417]
            temp2 = cv2.bitwise_or(temp,temp1)
            frame[143:390,203:417] = temp2

            #Red dots representing extreme points and remaining dots are corner points
            #cv2.circle(frame,(203+bottommost[0]+50,143+bottommost[1]),10,[0,255,255],-1)
            cv2.circle(temp2,bottommost,5,[0,0,255],-1)
            cv2.circle(temp2,rightmost,5,[0,0,255],-1)
            cv2.circle(temp2,topmost,5,[0,0,255],-1)
            cv2.circle(temp2,leftmost,5,[0,0,255],-1)

            #Finding slope of rightmost,topmost,leftmost point with respect to bottommost point
            angr = math.atan((bottommost[1]-rightmost[1])/(bottommost[0]-rightmost[0]))
            angt = math.atan((bottommost[1]-topmost[1])/(bottommost[0]-topmost[0]))
            angl = math.atan((bottommost[1]-leftmost[1])/(bottommost[0]-leftmost[0]))
           
            #Finding relative angle between two adjacent sloping line
            ang0 = angt - angr
            ang1 = angl - angt
            #print("",ang0,ang1)

        #Using all above found stuff-slope,minimum_rectangle,coreners and oberving the output and setting a hard code range
    try:
        if (ang0 >=-0.80 and ang0 <= -0.70) and (ang1 >= 2.70 and ang1<=2.87) or len(corners)==7 and len1t>1100:
            cv2.putText(frame,"5",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-0.35 and ang0 <= -0.27) and (ang1 >= 2.70 and ang1<=2.82) and len(corners)==6 and len1t > 1050:
            cv2.putText(frame,"4",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        #if (ang0 >=-0.3 and ang0 <= -0.1) and (ang1 >= 2.50 and ang1<=2.80) and peri<700 and len(corners)==4:
            #cv2.putText(frame,"1",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if  len(corners)==4 and len1t<750:
            cv2.putText(frame,"1",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-1.2 and ang0 <= -0.80) and (ang1 >= 3.0 and ang1<=3.20) and len(corners)==5 and len1t<750:
            cv2.putText(frame,"6",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-0.45 and ang0 <= -0.30) and (ang1 >= 2.7 and ang1<=3.0) and len(corners)==5 and len1t>800 and len1t <1050 and (len(lines) == 4 or len(lines)==3 or len(lines) == 2) :
            cv2.putText(frame,"3",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-1.1 and ang0 <= -0.75) and (ang1 >=2.5  and ang1<=3.2) and len(corners)==5 and len1t >750 and len1t<900:
            cv2.putText(frame,"7",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-0.55 and ang0 <= -0.45) and ((ang1 >=2.5  and ang1<=2.65) or ang1==None) or  peri < 600 and len1t<600:
            cv2.putText(frame,"0",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        #if (ang0 >=-0.48 and ang0 <= -0.40) and (ang1 >=2.8  and ang1<=3.1) and len(corners)==4:
            #cv2.putText(frame,"2",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if  len(corners)==4 and len1t>750:
            cv2.putText(frame,"2",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-0.90 and ang0 <= -0.40) and (ang1 >=1  and ang1<=3.1) and len(corners)==6 and len1t>900 and len1t<1100:
            cv2.putText(frame,"8",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
        if (ang0 >=-0.8 and ang0 <= -0.5) and (ang1 >=2.5  and ang1<=3) and len1t<900 and len1t>600:
            cv2.putText(frame,"9",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
    except:
        pass
        #Old method 
        """if len(corners) == 7 :
            #time.sleep(1)
            #print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            cv2.putText(frame,"5",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
            #cv2.imshow("frame",frame)
            #time.sleep(0.05)
            
        elif len(corners) == 5 :
            if (len(lines) == 4 or len(lines)==3 or len(lines) == 2) and (len1t>=900):
                #time.sleep(0.033)
                cv2.putText(frame,"3",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
                #print("3")
            elif (len(lines) == 1 or len(lines) == 0) or peri < 600:
                cv2.putText(frame,"0",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
                #print("0")
            elif len1t >= 700 and len1t <= 850 :
                cv2.putText(frame,"7",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
            else :
                cv2.putText(frame,"6",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
                #print("6")
        elif len(corners) == 4:
            if len1t >= 750 :
                cv2.putText(frame,"2",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
            elif len1t >=450 :
                cv2.putText(frame,"1",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
        elif len(corners) == 6:
            if  len1t >= 600 and len1t <= 750 :
                cv2.putText(frame,"9",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
            elif len1t >=900 and len1t<= 1050 :
                cv2.putText(frame,"8",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
            elif len1t > 1050 :
                cv2.putText(frame,"4",(550,450),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame",frame)
    except:
        cv2.putText(frame,"NOT DETECTED",(200,450),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        #cv2.imshow("frame",frame)
        #print("put hand properely")"""
    
    #Finally displaying the frame
    cv2.imshow("frame",frame)
    #count += 1
    time.sleep(0.033)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()