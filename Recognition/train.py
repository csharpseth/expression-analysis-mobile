import os
import cv2 as cv
import numpy as np

categories = ['positive', 'negative', 'neutral']
DIR = os.path.join('C:', '/', 'train')

leftEyeHaar = cv.CascadeClassifier('HAAR/haar_lefteye.xml')
rightEyeHaar = cv.CascadeClassifier('HAAR/haar_righteye.xml')
faceHaar = cv.CascadeClassifier('HAAR/haar_face.xml')

facialFeatures = []
facialLabels = []

leftEyeFeatures = []
leftEyeLabels = []

rightEyeFeatures = []
rightEyeLabels = []

def increase_brightness(img, value=30):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img

def getClosestEye(rect, padding=0):
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

    return (start_x-padding, start_y-padding, width+padding, height+padding)

def create_train():
    print(' ------- Training Set Initialized ------- ')
    for state in categories:
        path = os.path.join(DIR, state)
        path = path.replace("\\", '/')
        label = categories.index(state)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)
            img_path = img_path.replace("\\", '/')

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            left_eyes_rect = leftEyeHaar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=32)
            right_eyes_rect = rightEyeHaar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=32)
            faces_rect = faceHaar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=12)
            
            if(len(left_eyes_rect) > 0):
                (leftX, leftY, leftW, leftH) = getClosestEye(left_eyes_rect)
                left_roi = gray[leftY:leftY+leftH, leftX:leftX+leftW]
                leftEyeFeatures.append(left_roi)
                leftEyeLabels.append(label)

            if(len(right_eyes_rect) > 0):
                (rightX, rightY, rightW, rightH) = getClosestEye(right_eyes_rect)
                right_roi = gray[rightY:rightY+rightH, rightX:rightX+rightW]
                rightEyeFeatures.append(right_roi)
                rightEyeLabels.append(label)

            if(len(faces_rect) > 0):
                (faceX, faceY, faceW, faceH) = getClosestEye(faces_rect)
                face_roi = gray[faceY:faceY+faceH, faceX:faceX+faceW]
                facialFeatures.append(face_roi)
                facialLabels.append(label)
            
            print(f'Labeled {img_path} as {state}')

create_train()

print(' ------- Training Set Created ------- ')

leftEyeFeatures = np.array(leftEyeFeatures, dtype="object")
leftEyeLabels = np.array(leftEyeLabels)

print(' ------- Created Left Eye Training Set ------- ')

rightEyeFeatures = np.array(rightEyeFeatures, dtype="object")
rightEyeLabels = np.array(rightEyeLabels)

print(' ------- Created Right Eye Training Set ------- ')

facialFeatures = np.array(facialFeatures, dtype="object")
facialLabels = np.array(facialLabels)

print(' ------- Created Face Training Set ------- ')

print(' ------- Training Initialized ------- ')

left_recognizer = cv.face.LBPHFaceRecognizer_create()
left_recognizer.train(leftEyeFeatures, leftEyeLabels)

print(' ------- Trained Left Eye ------- ')

right_recognizer = cv.face.LBPHFaceRecognizer_create()
right_recognizer.train(rightEyeFeatures, rightEyeLabels)

print(' ------- Trained Right Eye ------- ')

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(facialFeatures, facialLabels)

print(' ------- Trained Face ------- ')

print(' ------- Training Completed ------- ')

print(' ------- Saving... ------- ')

left_recognizer.save('DATA/sentiment_set_lefteye.yml')
np.save('DATA/sentiment_set_lefteye_features.npy', leftEyeFeatures)
np.save('DATA/sentiment_set_lefteye_labels.npy', leftEyeLabels)

print(' ------- Saved Left Eye ------- ')

right_recognizer.save('DATA/sentiment_set_righteye.yml')
np.save('DATA/sentiment_set_righteye_features.npy', rightEyeFeatures)
np.save('DATA/sentiment_set_righteye_labels.npy', rightEyeLabels)

print(' ------- Saved Right Eye ------- ')

face_recognizer.save('DATA/sentiment_set_face.yml')
np.save('DATA/sentiment_set_face_features.npy', facialFeatures)
np.save('DATA/sentiment_set_face_labels.npy', facialLabels)

print(' ------- Saved Face ------- ')

print(' ------- Saved! ------- ')