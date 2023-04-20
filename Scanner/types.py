# Custom type definitions

from typing import Union

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