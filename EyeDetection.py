#Import All Libraries 
import cv2
import numpy as np
import time
import socket

###Defines client as the socket
client = socket.socket()
##
##
###Connect's to Pi through IP adress and port
client.connect(('10.202.7.219', 2345)) #Schools IP
##client.connect(('10.0.0.188',2345))  #Homes IP 

centerCal = -1      #Center Calibration Variable
calLeft = 0         #Left Calibration Variable
calRight = 0        #Right Calibration Variable
calUp = 0           #Up Calibration Variable
intialX = 0         #X position
intialY = 0         #Y Position 
intialYup = 0       #Up Limit 
intialXleft = 0     #Left Limit
intialXright = 0    #Right Limit
tcount = 0          #Blink Count
timetotal = 0       #Timer Total
tstartcount = 0     #Start Timer Variable
tstopcounter = 0    #Stop Timer Variable
rightCount = 0      #Total Number of Times turned Right
leftCount = 0       #Total Number of Times turned Left
upCount = 0         #Total Number of Times going Forward
brakeCount = 0      #Total Number of Times braking
count = 0           #Counting Number of Points for Calibration
tstart2 = 0         #Starting Timer 
 

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml") #Use for Face Recgonition
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml") #Use for eye Recgonition 

cap = cv2.VideoCapture(0)# 1 = USB Camera 0 = Webcam
while True:

    xCenter = 0  
    ret, img = cap.read() #Read Camera
    img2 = cv2.flip(img, 1) #Flip image for proper orientation
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) #Convert to grayscale

    eyes = eyeCascade.detectMultiScale(gray, 3.3,8) #Use classifier to detect eyes
        
                   
    for (ex,ey,ew,eh) in eyes:
    

      if (ex > 300 ):    #Select 1 eye

            
        cv2.rectangle(img2, (ex,ey), (ex+ew, ey+eh), (255,0,0), 2) #Box Eye
        xCenter = ((ex+ew) + ex)/2  #Center of eye X direction
        yCenter = ((ey+eh) + ey)/2 #Ceneter of eye y direction
        cv2.circle(img2, (xCenter,yCenter), 5, (0,0,255),-1) #circle iris 
            

#We begin to do center calibration
        if (centerCal== -1):
            print "Center Calibration: Please look into camera"
            time.sleep(4)
            centerCal = 1
        if (centerCal == 1):        #Gather 10 center locations
            if (count < 10):
                X = xCenter
                Y = yCenter
                intialX = intialX + X
                intialY = intialY + Y
                count = count + 1
                print count

            if (count == 10):       #Find average center location
                intialX = intialX/10
                intialY = intialY/10
                print 'Center Calibration Complete'
                centerCal = 0
                calLeft = 1
                count = 0
                print 'Left Calibration: Please look left'
                time.sleep(4)
            

#We begin to do left calibration
        if (calLeft == 1):          #Gather 10 left locations
            if (count < 10):
                X = xCenter
                intialXleft = intialXleft + X
                print count
                count = count + 1

            if (count == 10):       #Find average left location
                intialXleft = intialXleft/10
                count = 0
                calLeft = 0
                calRight = 1
                print 'Left calibration is complete'
                print 'Right calibration: Please look right'
                time.sleep(4)

#We begin to do right calibration 

        if (calRight == 1):         #Gather 10 right locations
            if (count < 10):
                X = xCenter
                intialXright = intialXright + X
                print count
                count = count + 1

            if (count == 10):       #Find average right location
                intialXright = intialXright/10
                count = 0
                calRight = 0
                calUp = 1
                print 'Right calibration is complete'
                print 'Forward/Backward Calibration: Please look up'
                time.sleep(4) 

#We begin to do calibration for both forward and backward calibration

        if (calUp == 1):            #Gather 10 up locations
            if (count < 10):
                Y = yCenter
                intialYup = intialYup + Y
                print count
                count = count + 1

            if (count == 10):       #Gather average up location
                intialYup = intialYup/10
                count = 0
                calUp = 0
                centerCal = 2
                print 'Calibration Complete: to begin please blink twice to move'
                time.sleep(2) 
            

        if (centerCal == 2): #After Calibration
            xLeft = intialXleft  #Setting X left direction limit
            xRight = intialXright #Setting X right direction limit
            yUp = intialYup #Setting Y up direction limit 
            
            if (tcount == 2):

                if (xCenter < xLeft): #If X cordinate is less than left average move left
                    if (yCenter > yUp):
                        if (upCount == 0):
                            if (rightCount == 0):
                                print 'Turn Left'
                                client.send("Left")     #Sending Left to the Pi
                                leftCount = leftCount + 1
                                brakeCount = 1 + brakeCount
                                tstart2 = 1
                        
                if (xCenter > xRight):  #If X cordinate is greather than right average move right 
                    if (yCenter > yUp):
                        if (upCount == 0):
                            if (leftCount == 0):
                                print 'Turn Right'
                                client.send("Right")    #Sending Right to the Pi
                                rightCount = rightCount + 1
                                brakeCount = 1 + brakeCount 
                                tstart2 = 1

                if (yCenter < yUp):     #If Y cordinate is less than the up average move forward
                    if (xCenter < xRight):
                        if (xCenter > xLeft):
                            if (leftCount == 0):
                                if (rightCount == 0):
                                    print 'Forwards'
                                    client.send("Forward")  #Sending Forward to the Pi
                                    brakeCount= 1 + brakeCount
                                    upCount = upCount + 1 
                                    tstart2 = 1

                            
                if (yCenter > yUp):     #If eye position is in middle of eye then brake
                    if (xCenter < xRight):
                        if (xCenter > xLeft):
                            if (brakeCount > 0):
                                print 'Brake'
                                client.send("Brake")    #Sending Brake to the Pi 
                                rightCount = 0
                                leftCount = 0
                                upCount = 0 
                                tcount = 0
                                brakeCount = 0
                                tstart2 = 0

            if (tcount == 68):
                if (yCenter < yUp):     #If Y cordinate is less than the up average move backward
                            print 'Backwards'
                            client.send("Backwards")    #Sending Backwards to the Pi
                            brakeCount = 1 + brakeCount
                            tstart2 = 1


                            
                if (yCenter > yUp):     #If eye position is in middle of eye then brake
                    if (brakeCount > 0):
                            print 'Brake'
                            client.send("Brake")    #Sending Brake to the Pi 
                            tcount = 0
                            brakeCount = 0
                            tstart2 = 0
                            tcount = 0
                            brakeCount = 0
        
    if (centerCal == 2):
        if (xCenter == 0):  #If eye is closed then start timer
            if (tstartcount == 0):
                if (tstart2 == 0):
                    tstart = time.time()    #Start Time
                    tstartcount = tstartcount + 1
                    tstopcounter = tstopcounter + 1

        else:
            if (tstopcounter == 1): #When eye opens calculate total time the eye was closed
                tstop = time.time()         #Stop Time
                timetotal = tstop - tstart  #Calculating total time 
                tstartcount = 0
                tstopcounter = 0

        if (timetotal > 2):     #If eye was closed for more than 2 seconds count that as one blink
            tcount = tcount + 1
            print tcount
            if (tcount == 2):   #If eye blinks twice then enable movement
                print 'Select Direction'
                time.sleep(4)
            if (timetotal > 5): #If eye is closed for more than 5 seconds enable backwards movement
                print 'Look Up to move backwards'
                time.sleep(4) 
                tcount = 68
            timetotal = 0
            if (tcount == 3 ): #Safety feature to apply brake if counter ever reaches 3
                print 'Brake'
 #               send.client("Brake")    #Sending Brake to the Pi 
                rightCount = 0
                leftCount = 0
                upCount = 0 
                tcount = 0
                brakeCount = 0
                tstart2 = 0
 
    cv2.imshow('Image', img2) #Display image
    k = cv2.waitKey(30) & 0xff #Exit the program by pressing the escape button
    if k ==27:
        break

cap.release()               #Release the camera
cv2.destroyAllWindows()     #Destroy open windows
