import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceproject-6ef6d-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceproject-6ef6d.appspot.com"
})