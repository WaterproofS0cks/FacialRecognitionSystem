import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceproject-6ef6d-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceproject-6ef6d.appspot.com"
})

#importing students' images from images by using the same logic as earlier
folderPathImages = 'Images'
listPathImages = os.listdir(folderPathImages)
imgListImages = []

#extracting the studentIDs from each picture
studentIDs = []

for path in listPathImages:
    imgListImages.append(cv2.imread(os.path.join(folderPathImages, path)))
    studentIDs.append(os.path.splitext(path)[0])

    fileName = f'{folderPathImages}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def generateEncodings(images):

    encodingsList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodingsList.append(encode)

    return encodingsList

encodingsListKnown = generateEncodings(imgListImages)
encodingsListWithIDS = [encodingsListKnown, studentIDs]

encodingFile = open("EncodingsFile.p", "wb")
pickle.dump(encodingsListWithIDS, encodingFile)
encodingFile.close()
