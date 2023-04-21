from .types import SerialMessage, QRPayload

import serial
import time

class Scanner:
  def __init__(self, port:str, baudrate:int) -> None:
    self.PORT = port
    self.BAUDRATE = baudrate
    self.TIMEOUT = 0.11 # read timeout (1/9)s

    self.ser = None
    self.serialMsgStart = SerialMessage('<qr>')
    self.serialMsgEnd = SerialMessage('</qr>')

    self.is_ready = False

    self.__serialConnect()
  
  def __serialConnect(self) -> None:
    while self.ser is None:
      try:
        print(f"Attempting serial connection to QR scanner at port '{self.PORT}' (baudrate: '{self.BAUDRATE}')")
        self.ser = serial.Serial(port=self.PORT, baudrate=self.BAUDRATE, timeout=self.TIMEOUT)
        print("! Serial connection established.")
      except serial.SerialException as err:
        print("! SerialException occured.")
        print("Trying again...\n")
        time.sleep(1)
        self.is_ready = False

    if self.ser.is_open:
      print("! Scanner ready.\n")
      self.is_ready = True
  
  def readNext(self) -> QRPayload:
    if self.ser is None or not self.ser.is_open:
      print("! Unable to access serial connection to Scanner.")
      print("Trying to esatblish connection again...\n")
      self.__serialConnect()
      self.readNext()

    x = self.ser.read_until(self.serialMsgStart.bytes)
    while x != self.serialMsgStart.bytes:
      x += self.ser.read(1)
      time.sleep(0.05)

    status = self.ser.read(1)
    status = int(status or '0')
    
    msg = self.ser.read_until(self.serialMsgEnd.bytes)
    while msg[-5:] != self.serialMsgEnd.bytes:
      msg += self.ser.read(1)
      time.sleep(0.05)

    msg = msg.decode().replace(self.serialMsgEnd.str, '')

    return QRPayload(status, msg)
  
  def close(self) -> None:
    if self.ser is not None:
      self.ser.close()
    
    self.is_ready = False
