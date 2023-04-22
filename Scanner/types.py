# Custom type definitions

from typing import Union
import re

class SerialMessage:
  def __init__(self, msg:Union[str, bytes]):
    if isinstance(msg, str):
      self.bytes = msg.encode()
      self.str = msg
    elif isinstance(msg, bytes):
      self.bytes = msg
      self.str = msg.decode()
  
  def __str__(self):
    return self.str

class QRPayload:
  def __init__(self, status:int , data:str):
    self.status = status
    self.data = data
  
  def __str__(self):
    return self.data

class StudentQR:
  def __init__(self, payload:QRPayload):
    if payload.status == 0:
      raise ValueError("Error scanning QR.")
    
    data = payload.data.split('\n')
    if len(data) != 3:
      raise ValueError("Invalid QR")

    checks = [
      len(data[0]) != 0,
      re.search('^[0-9]{4}[a-zA-Z]{2}[0-9]{2}$'.upper(), data[1]),
      re.search('^[a-b0-9]{32}$', data[2])
    ]
    
    if not all(checks):
      raise ValueError("Invalid QR")
    
    self.name = data[0].upper()
    self.roll_no = data[1].upper()
    self.hash = data[2]
  
  def __eq__(self, __value:object) -> bool:
    if not isinstance(__value, StudentQR):
      return False

    if self.name == __value.name and self.roll_no == __value.roll_no and self.hash == __value.hash:
      return True

    return False