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
).init()

scanner = Scanner(
  port=str(os.environ['SCANNER_PORT']),
  baudrate=str(os.environ['SCANNER_BAUDRATE'])
)

lastValidScan = None
scanCount = 0
while servo.is_ready and scanner.is_ready:
  scan = scanner.readNext()

  if scan.status == 1:
    if lastValidScan is None and scan != lastValidScan:
      lastValidScan = scan
      helpers.handleNewScan(scan)
    elif scan.data == lastValidScan:
      helpers.handleDuplicateScan()
