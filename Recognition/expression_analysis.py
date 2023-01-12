import numpy as np
import cv2 as cv
import requests

#Live Feed
capture = cv.VideoCapture(0)
drawWindow = True
showDebug = True

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def changeRes(width, height):
    capture.set(3, width)
    capture.set(4, height)
    
def increase_brightness(img, value=30):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img

def getClosest(rect):
    start_x = 0
    start_y = 0
    width = 0
    height = 0

    #iterates through all of the detected faces and picks the closest one based on the size of the rectangle
    for (x,y,w,h) in rect:
        if (w>=width):
            width = w
            height = h
            start_x = x
            start_y = y

    return (start_x, start_y, width, height)

def determineOveralSentiment(left, right, face):
    positive = 0
    negative = 0
    neutral = 0

    if(left == 0): positive = positive+1
    if(right == 0): positive = positive+1
    if(face == 0): positive = positive+1

    if(left == 1): negative = negative+1
    if(right == 1): negative = negative+1
    if(face == 1): negative = negative+1

    if(left == 2): neutral = neutral+1
    if(right == 2): neutral = neutral+1
    if(face == 2): neutral = neutral+1

    if(positive>=neutral and positive>negative):
        return categories[0]
    elif(negative>=neutral and negative>positive):
        return categories[1]
    
    return categories[2]

changeRes(300, 300)

categories = ['positive', 'negative', 'neutral']

leftEyeHaar = cv.CascadeClassifier('HAAR/haar_lefteye.xml')
rightEyeHaar = cv.CascadeClassifier('HAAR/haar_righteye.xml')
faceHaar = cv.CascadeClassifier('HAAR/haar_face.xml')

left_recognizer = cv.face.LBPHFaceRecognizer_create()
right_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer = cv.face.LBPHFaceRecognizer_create()

left_recognizer.read('DATA/sentiment_set_lefteye.yml')
right_recognizer.read('DATA/sentiment_set_righteye.yml')
face_recognizer.read('DATA/sentiment_set_face.yml')

leftEyeFeatures = np.load('DATA/sentiment_set_lefteye_features.npy', allow_pickle=True)
leftEyeLabels = np.load('DATA/sentiment_set_lefteye_labels.npy', allow_pickle=True)

rightEyeFeatures = np.load('DATA/sentiment_set_righteye_features.npy', allow_pickle=True)
rightEyeLabels = np.load('DATA/sentiment_set_righteye_labels.npy', allow_pickle=True)

facialFeatures = np.load('DATA/sentiment_set_face_features.npy', allow_pickle=True)
facialLabels = np.load('DATA/sentiment_set_face_labels.npy', allow_pickle=True)

while True:
    isTrue, frame = capture.read()

    #Brighten
    frame = increase_brightness(frame, 20)

    #convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #find all faces in the given frame
    left_eyes_rect = leftEyeHaar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=32)
    right_eyes_rect = rightEyeHaar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=32)
    face_rect = faceHaar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=12)

    leftLabel = 2
    rightLabel = 2
    faceLabel = 2
    sentiment = 'none'
    
    (leftX, leftY, leftW, leftH) = getClosest(left_eyes_rect)
    (rightX, rightY, rightW, rightH) = getClosest(right_eyes_rect)
    (faceX, faceY, faceW, faceH) = getClosest(face_rect)

    if(len(left_eyes_rect) > 0):
        left_roi = gray[leftY:leftY+leftH, leftX:leftX+leftW]
        label, confidence = left_recognizer.predict(left_roi)
        leftLabel = label

    if(len(right_eyes_rect) > 0):
        right_roi = gray[rightY:rightY+rightH, rightX:rightX+rightW]
        label, confidence = right_recognizer.predict(right_roi)
        rightLabel = label

    if(len(face_rect) > 0):
        face_roi = gray[faceY:faceY+faceH, faceX:faceX+faceW]
        label, confidence = face_recognizer.predict(face_roi)
        faceLabel = label

    sentiment = determineOveralSentiment(leftLabel, rightLabel, faceLabel)

    if(drawWindow == True):
        if(showDebug == True):
            #draw a rectangle around every detected face
            cv.rectangle(frame, (leftX,leftY), (leftX+leftW,leftY+leftH), (0, 255, 0), thickness=1)
            cv.rectangle(frame, (rightX,rightY), (rightX+rightW,rightY+rightH), (255, 0, 0), thickness=1)
            cv.rectangle(frame, (faceX,faceY), (faceX+faceW,faceY+faceH), (0, 0, 255), thickness=1)

            #Background
            cv.rectangle(frame, (0,0), (180,54), (0,0,0), -1)
            #Is a face detected label
            cv.putText(frame, f'Left Sentiment: {categories[leftLabel]}', (6, 12), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)
            #The current sentiment of a detected face
            cv.putText(frame, f'Right Sentiment: {categories[rightLabel]}', (6, 24), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)
            #The confidence of that sentiment
            cv.putText(frame, f'Facial Sentiment: {categories[faceLabel]}', (6, 36), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)
            cv.putText(frame, f'Overall Sentiment: {sentiment}', (6, 48), cv.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), thickness=1)

        cv.imshow('Facial Sentiment Analysis', frame)

        if(cv.waitKey(20) & 0xFF==ord('d')):
            break
    else:
        print('Running...')
        if(input() == 'stop'):
            break

capture.release()
cv.destroyAllWindows()