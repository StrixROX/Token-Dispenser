from Servo import ServoController as Servo
from Scanner import Scanner
import helpers

import os

servo = Servo(
  PWM=int(os.environ['SERVO_PWM_PIN']),
  freq=int(os.environ['SERVO_PWM_FREQ']),
  dc_min=float(os.environ['SERVO_DC_MIN']),
  dc_neut=float(os.environ['SERVO_DC_NEUT']),
  dc_max=float(os.environ['SERVO_DC_MAX'])
)
servo.init()

scanner = Scanner(
  port=str(os.environ['SCANNER_PORT']),
  baudrate=str(os.environ['SCANNER_BAUDRATE'])
)

lastValidScan = None
while servo.is_ready and scanner.is_ready:
  try:
    scan = scanner.readNext()

    if scan.status == 1:
      if lastValidScan is None or scan != lastValidScan:
        lastValidScan = scan
        helpers.handleNewScan(servo, scan)
  except:
    servo.cleanup()
