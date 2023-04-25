from Servo import ServoController as Servo
from Scanner import Scanner
from LED import LEDController
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

indicatorLEDs = {
  'green': LEDController(11),
  'red': LEDController(13)
}
for led in indicatorLEDs.values():
  led.init()

lastValidScan = None
while servo.is_ready and scanner.is_ready:
  try:
    scan = scanner.readNext()

    if scan.status == 1:
      if lastValidScan is None or scan != lastValidScan:
        lastValidScan = scan
        helpers.handleNewScan(servo, indicatorLEDs, scan)
  except:
    servo.cleanup()
    for led in indicatorLEDs.values():
      led.cleanup()
