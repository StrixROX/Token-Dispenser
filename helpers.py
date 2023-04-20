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

def saveToDatabase(data:QRPayload):
  # logic to save data to database
  print("Saving to DB")

def handleInvalidScan():
  # logic to handle invalid qr being scanned
  print("Invalid QR code")

def handleDuplicateScan():
  print("QR already scanned.")

def handleNewScan(data:QRPayload):
  is_valid = validateQRData(data)
  
  if is_valid:
    saveToDatabase(data)
  else:
    handleInvalidScan()