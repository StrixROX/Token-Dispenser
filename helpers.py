from Servo import ServoController
from Scanner.definitions import QRPayload, StudentQR
from DatabaseConnector import DatabaseConnector
from definitions import MealTimings

import os
import datetime
import time

#creating an instance DatabaseConnector
db = DatabaseConnector(os.environ['DB_NAME'])
registeredStudents = db.getTable('registered_students')

def dropNextToken(servo:ServoController) -> None:
  # For sinlge hole disc
  # if servo.position == 0:
  #   servo.setAngle(90, mode=2)
  # elif servo.position == -90:
  #   servo.setAngle(0, mode=2)
  #   time.sleep(0.5)
  #   servo.setAngle(90, mode=2)
  # elif servo.position == 90:
  #   servo.setAngle(0, mode=2)
  #   time.sleep(0.5)
  #   servo.setAngle(-90, mode=2)

  # For double hole disc
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

# def clearTable(tableName: str):
#   db.__cur.execute(f"DELETE FROM {tableName}")
#   db.__db.commit()
#   print(f"The table '{tableName}' has been cleared.")

def logScan(qr:StudentQR) -> bool:
  now = datetime.datetime.now()
  mealSlots = MealTimings(is_weekend=(now.weekday() < 5)).slots

  # check if current time is within any meal slot
  nowTime = now.time()
  for slot in mealSlots:
    slotStart = datetime.datetime.strptime(slot[0], '%H:%M:%S').time()
    slotEnd = datetime.datetime.strptime(slot[1], '%H:%M:%S').time()
    if eval(os.environ['IS_DEMONSTRATION']) or slotStart <= nowTime <= slotEnd:
        # check if QR code exists in the table
        if db.scanIsLogged(qr):
          return False

        return db.logScan(qr, now)

    print("Not within meal time slot.")
  return False

  # TODO: when to clear the meal_attendance table
  # suggestion: linux cronjob

def handleInvalidScan(level:int, indicatorLEDs:dict) -> None:
  # level 1: qr itself is not a valid StudentQR
  # level 2: qr is valid StudentQR but it is not registered in the db
  # level 3: qr is valid StudentQR and student is registered in the db
  # but qr is already scanned
  # level 4: any other error

  print("Invalid QR code:", level)
  indicatorLEDs['green'].setState(1)
  time.sleep(0.5)
  indicatorLEDs['green'].setState(0)
  time.sleep(0.5)
  indicatorLEDs['green'].setState(1)
  time.sleep(0.5)
  indicatorLEDs['green'].setState(0)

def handleNewScan(servo:ServoController, indicatorLEDs:dict, payload:QRPayload) -> None:
  try:
    qr = StudentQR(payload)

    is_registered = checkRegistered(qr)
    if not is_registered:
      handleInvalidScan(2, indicatorLEDs)

    did_save = logScan(qr)
    if did_save:
      dropNextToken(servo)
      indicatorLEDs['green'].setState(1)
      time.sleep(1)
      indicatorLEDs['green'].setState(0)
    else:
      handleInvalidScan(3, indicatorLEDs)
  except ValueError:
    handleInvalidScan(1, indicatorLEDs)
  except:
    handleInvalidScan(4, indicatorLEDs)
