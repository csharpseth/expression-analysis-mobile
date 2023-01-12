"""
This script allows you to take video frames and save them as images for training data

'Iteration' is used as the filename index. I set this up if I take multiple sets of pictures
(To account for the pictures I've already take)

'label' is exactly how it sounds, it's a label

Ex:
iteration = 100 && label = 'happy' the output image will be labeled: "happy_100.jpg"
"""

import cv2 as cv

#Reading Videos
capture = cv.VideoCapture(0)

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def changeRes(width, height):
    capture.set(3, width)
    capture.set(4, height)

changeRes(1024, 1024)

haar_cascade = cv.CascadeClassifier('haar_face.xml')
isFace = False
iteration = 1
label = 'neutral'

while True:
    isTrue, frame = capture.read()
    #frame_resized = rescaleFrame(frame, 0.5)
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)

    start_x = 0
    start_y = 0
    width = 0
    height = 0

    if (len(faces_rect) > 0):
        isFace = True
    else:
        isFace = False

    if (isFace == True):
        for (x,y,w,h) in faces_rect:
        #cv.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), thickness=2)
            if (w>=width):
                width = w
                height = h
                start_x = x
                start_y = y
        iteration+=1
        path = "img/%s_%s.jpg" % (label, iteration)
        cv.imwrite(path, frame)
        cv.rectangle(frame, (start_x,start_y), (start_x+width,start_y+height), (0, 255, 0), thickness=1)

    cv.rectangle(frame, (0,0), (160,20), (0,0,0), -1)
    cv.putText(frame, f'Face Detected: {isFace}', (6, 12), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)

    cv.imshow('face detect', frame)

    if(cv.waitKey(20) & 0xFF==ord('d')):
        break

capture.release()
cv.destroyAllWindows()