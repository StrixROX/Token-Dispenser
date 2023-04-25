#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class LEDController:
  def __init__(self, GPIO_PIN:int) -> None:
    self.GPIO_PIN = GPIO_PIN

    self.is_ready = False
    self.state = False # False = off | True = on

  def init(self) -> bool:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.GPIO_PIN, GPIO.OUT)

    for i in range(2):
      # blink twice
      GPIO.output(self.GPIO_PIN, GPIO.HIGH)
      time.sleep(1)
      GPIO.output(self.GPIO_PIN, GPIO.LOW)
      time.sleep(1)

    print("LED ready.")
    
    self.is_ready = True
    self.state = False

    return self.is_ready

  def cleanup(self) -> None:
    print("Cleaning up...")
    GPIO.cleanup()
    print("Cleanup complete.")

    self.is_ready = False
  
  def setState(self, state:bool):
    GPIO.output(self.GPIO_PIN, GPIO.HIGH if state else GPIO.LOW)
