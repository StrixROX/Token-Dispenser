from Servo import ServoController
from Scanner.types import QRPayload, StudentQR
from DatabaseConnector import DatabaseConnector

#creating an instance DatabaseConnector
db = DatabaseConnector()

registeredStudents = db.getTable('registered_students')
if registeredStudents is None:
  # Create new registered_students table
  query = "CREATE TABLE IF NOT EXISTS registered_students (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, roll_number TEXT NOT NULL, qrcode TEXT NOT NULL);"
  registeredStudents = db.createTable(query)

def dropNextToken(servo:ServoController) -> None:
  if servo.position == 0:
    servo.setAngle(90, mode=2)
  elif servo.position == 90:
    servo.setAngle(0, mode=2)

def checkRegistered(qr:StudentQR) -> bool:
  # TODO: optimize search
  for stud in registeredStudents:
    if stud['roll_number'] == qr.roll_no.upper() and stud['qrcode'] == qr.hash:
      return True

  return False

def logScan(qr:StudentQR) -> bool:
  # TODO: log scan if not scanned already for current meal
  return True

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
