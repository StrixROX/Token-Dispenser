from Servo import ServoController as Servo
from Scanner import Scanner
import time
import os

myServo = Servo(
  PWM=os.environ['SERVO_PWM_PIN'],
  freq=os.environ['SERVO_PWM_FREQ'],
  dc_min=os.environ['SERVO_DC_MIN'],
  dc_neut=os.environ['SERVO_DC_NEUT'],
  dc_max=os.environ['SERVO_DC_MAX']
)
myServo.init()

# servo testing code
myServo.setAngle(0)
time.sleep(1)
myServo.setAngle(90)
time.sleep(1)
myServo.setAngle(180)
time.sleep(1)
myServo.setAngle(90)
time.sleep(1)
myServo.setAngle(0)
time.sleep(1)

myServo.cleanup()

# scanner testing code
myScanner = Scanner(os.environ['SCANNER_PORT'], os.environ['SCANNER_BAUDRATE'])

prevScan = None
while True:
  scan = myScanner.readNext()
  
  if(scan.status == 1 and (prevScan is None or scan.data != prevScan.data)):
    prevScan = scan
    print(scan)