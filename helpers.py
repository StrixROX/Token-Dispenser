from Scanner.types import QRPayload

def validateQRData(data:QRPayload):
  # validation logic goes here
  return True

def saveToDatabase(data:QRPayload):
  # logic to save data to database
  pass

def handleInvalidScan():
  # logic to handle invalid qr being scanned
  pass

def handleDuplicateScan():
  print("QR already scanned.")
  pass

def handleNewScan(data:QRPayload):
  is_valid = validateQRData(data)
  
  if is_valid:
    saveToDatabase(data)
  else:
    handleInvalidScan()