from Servo import ServoController
from Scanner.types import QRPayload, StudentQR
from DatabaseConnector import DatabaseConnector
from typing import List
import sqlite3
import datetime
import os

#creating an instance DatabaseConnector
db = DatabaseConnector()

registeredStudents = db.getTable('registered_students')

if registeredStudents is None:
  # Create new registered_students table
  query = "CREATE TABLE IF NOT EXISTS registered_students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, roll_number TEXT NOT NULL, qrcode TEXT NOT NULL);"
  registeredStudents = db.createTable(query)

def dropNextToken(servo:ServoController) -> None:
  if servo.position == 0:
    servo.setAngle(90, mode=2)
  elif servo.position == 90:
    servo.setAngle(0, mode=2)

def checkRegistered(qr:StudentQR) -> bool:
  # optimize search
  for stud in registeredStudents:
    if stud['roll_number'] == qr.roll_no.upper() and stud['name'] == qr.name.upper() and stud['qrcode'] == qr.hash:
      return True

  return False

def clearTable(tableName: str):
  db.cursor.execute(f"DELETE FROM {tableName}")
  db.conn.commit()
  print(f"The table '{tableName}' has been cleared.")

def logScan(qr:StudentQR) -> bool:
  # TODO: log scan if not scanned already for current meal
  now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  day = now.strftime('%A')
  weekend = ['Saturday', 'Sunday']

  meal_slots_weekdays = [['7:45:00', '10:30:00'], ['12:15:00', '14:30:00'], ['19:45:00', '22:30:00']]
  meal_slots_weekends = [['7:45:00', '11:00:00'], ['12:15:00', '15:00:00'], ['19:45:00', '23:00:00']]

  if day in weekend:
    mealSlot = meal_slots_weekends
  else:
    mealSlot = meal_slots_weekdays

  # check if current time is within any meal slot
  now_time = now.time()
  for slot in mealSlots:
    start_time = datetime.strptime(slot[0], '%H:%M:%S').time()
    end_time = datetime.strptime(slot[1], '%H:%M:%S').time()
    if start_time <= now_time <= end_time:
        # check if QR code exists in the table
        db.cursor.execute(f"SELECT * FROM meal_attendance WHERE qrcode='{qr.hash}'")
        if db.cursor.fetchone():
            print("QR code already scanned.")
            return False

        # insert scan data into the meal_attendance table
        db.cursor.execute(f"INSERT INTO meal_attendance (roll_no, qrcode, timestamp) VALUES ({qr.roll_no}, '{qr.hash}', '{now}')")
        db.conn.commit()
        print(f"The scan data {qr} has been logged for {slot}.")
        return True

    print("Not within meal time slot.")
    return False

  # TODO: when to clear the meal_attendance table

def handleInvalidScan(level:int) -> None:
  # level 1: qr itself is not a valid StudentQR
  # level 2: qr is valid StudentQR but it is not registered in the db
  # level 3: qr is valid StudentQR and student is registered in the db
  # but qr is already scanned
  # level 4: any other error

  # TODO: logic to handle invalid qr being scanned
  # different LED codes go here
  print("Invalid QR code")

def handleNewScan(servo:ServoController, payload:QRPayload) -> None:
  try:
    qr = StudentQR(payload)

    is_registered = checkRegistered(qr)
    if not is_registered:
      handleInvalidScan(2)

    did_save = logScan(qr)
    if did_save:
      dropNextToken(servo)
    else:
      handleInvalidScan(3)
  except ValueError:
    handleInvalidScan(1)
  except:
    handleInvalidScan(4)
