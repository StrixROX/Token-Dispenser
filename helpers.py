from Servo import ServoController
from Scanner.types import QRPayload
from random import randint

def validateQRData(data:QRPayload):
  # validation logic goes here
  print("Checking QR")

  if randint(1,10) % 2 == 0:
    print("OK")
    return True
  else:
    print("NOT OK")
    return False

def dropNextToken(servo:ServoController):
  if servo.position == 0:
    servo.setAngle(90, mode=2)
  elif servo.position == 90:
    servo.setAngle(0, mode=2)

def saveToDatabase(data:QRPayload):
  # logic to save data to database
  print("Saving to DB")
  return True

def handleInvalidScan():
  # logic to handle invalid qr being scanned
  print("Invalid QR code")

def handleDuplicateScan():
  print("QR already scanned.")

def handleNewScan(servo:ServoController, data:QRPayload):
  is_valid = validateQRData(data)
  
  if is_valid:
    did_save = saveToDatabase(data)

    if did_save:
      dropNextToken(servo)
  else:
    handleInvalidScan()