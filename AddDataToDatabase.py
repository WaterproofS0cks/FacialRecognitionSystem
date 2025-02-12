import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceproject-6ef6d-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")

data = {
    "TP011111":
    {
        "name": "Lee Wen Han",
        "major": "CS(AI)",
        "starting_year": 2021,
        "total_attendance": 8, 
        "grades": "A",
        "year": 2,
        "last_attendance_taken": "2024-01-23 16:30:30",
    },
    "TP054321":
    {
        "name": "Elon Musk",
        "major": "Ruining Lives (LMAO)",
        "starting_year": 2020,
        "total_attendance": 100, 
        "grades": "A+",
        "year": 4,
        "last_attendance_taken": "2024-01-22 01:30:30",
    },
        "TP063338":
    {
        "name": "Dalton Gan",
        "major": "SE",
        "starting_year": 2020,
        "total_attendance": 64, 
        "grades": "A+",
        "year": 2,
        "last_attendance_taken": "2024-01-23 01:30:30",
    },
        "TP068713":
    {
        "name": "Suzanne Lai",
        "major": "CS(AI)",
        "starting_year": 2021,
        "total_attendance": 10, 
        "grades": "A+",
        "year": 2,
        "last_attendance_taken": "2024-01-23 1:30:30",
    },
        "TP012345":
    {
        "name": "Idk his name :(",
        "major": "CS(AI)",
        "starting_year": 2019,
        "total_attendance": 7, 
        "grades": "A+",
        "year": 1,
        "last_attendance_taken": "2024-01-23 1:30:30",
    },
}

for key, value in data.items():
    ref.child(key).set(value)