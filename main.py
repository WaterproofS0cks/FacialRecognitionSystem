#asdAD
import cv2 
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime 

cred = credentials.Certificate("serviceAccountKey.json")    

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceproject-6ef6d-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceproject-6ef6d.appspot.com"
})

bucket = storage.bucket()

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)
backgroundImg = cv2.imread('Resources/Background.png')

#importing images from Modes
folderPathMode = 'Resources/Modes'
listPathMode = os.listdir(folderPathMode)
imgListMode = []
print(listPathMode)

for path in listPathMode:
    imgListMode.append(cv2.imread(os.path.join(folderPathMode, path)))


encodingsFile = open("EncodingsFile.p", "rb")
encodingsListWithIDS =pickle.load(encodingsFile)
encodingsFile.close()

encodingsListKnown, studentIDs = encodingsListWithIDS
print(studentIDs)

modeType = 0
counter = 0
id = -1

while True:
    success, image = capture.read()

    backgroundImg[162:162 + 480, 55:55 + 640] = image
    #overlay the FIRST element within the imgListMode on top of the background
    backgroundImg[44:44 + 633, 808:808 + 414] = imgListMode [modeType]

    #resize image
    smallImage = cv2.resize(image, (0,0), None, 0.25, 0.25)
    smallImage = cv2.cvtColor(smallImage, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(smallImage)
    encodeCurrentFrame = face_recognition.face_encodings(smallImage, faceCurrentFrame)

    if faceCurrentFrame:

        for encodeFace, facelocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches= face_recognition.compare_faces(encodingsListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodingsListKnown, encodeFace)
            matchIndex= np.argmin(faceDistance)
        
            if matches[matchIndex]:
                print("Registered Student Detected")
                print(studentIDs[matchIndex])
            
                y1, x2, y2, x1 = facelocation
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                backgroundImg = cvzone.cornerRect(backgroundImg, bbox, rt = 0)
                id = studentIDs[matchIndex]

                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:
                    
            if counter == 1:
                #Retrieving student's info from database
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                #Retrieving student's image from storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                studentImg = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #Update attendance record and data
                datetimeObject = datetime.strptime(studentInfo['last_attendance_taken'],
                                                "%Y-%m-%d %H:%M:%S")
                timeInSecsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(timeInSecsElapsed)
                
                ref = db.reference(f'Student/{id}')
                studentInfo['total_attendance'] += 1

                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_taken').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType = 3
                counter = 0
                backgroundImg[44:44 + 633, 808:808 + 414] =imgListMode[modeType]
            
            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                backgroundImg[44:44 + 633, 808:808 + 414] = imgListMode[modeType]

                if counter < 10:

                    cv2.putText(backgroundImg, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1),
                    cv2.putText(backgroundImg, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1),
                    cv2.putText(backgroundImg, str(studentInfo['grades']), (910, 625),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100,100,100), 1),
                    cv2.putText(backgroundImg, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100,100,100), 1),
                    cv2.putText(backgroundImg, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100,100,100), 1)

                    (width, height), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_SIMPLEX,1,1)

                    center_offset = (414 - width)//2
                    cv2.putText(backgroundImg, str(studentInfo['name']), (808 + center_offset,445),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)
                
                    backgroundImg[175:175 + 216, 909:909 + 216] = studentImg
                        
            counter += 1

            if counter > 20:
                counter = 0
                modeType = 0
                studentInfo = []
                studentImg = []
                backgroundImg[44:44 + 633, 808:808 + 414] = imgListMode[modeType]

    cv2.imshow("Attendance System", backgroundImg)
    cv2.waitKey(1)
