from Servo import ServoController as Servo
from Scanner import Scanner
from LED import LEDController as LED
import time
import os

# servo testing code
myServo = Servo(
  PWM=int(os.environ['SERVO_PWM_PIN']),
  freq=int(os.environ['SERVO_PWM_FREQ']),
  dc_min=float(os.environ['SERVO_DC_MIN']),
  dc_neut=float(os.environ['SERVO_DC_NEUT']),
  dc_max=float(os.environ['SERVO_DC_MAX'])
)
myServo.init()

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

# LED testing code
myLED = LED(11)
myLED.init()

print(f"Testing LED at PIN: {myLED.GPIO_PIN}.")
for i in range(3):
  myLED.setState(True)
  time.sleep(0.5)
  myLED.setState(False)
  time.sleep(0.5)

myLED.cleanup()

# scanner testing code
myScanner = Scanner(os.environ['SCANNER_PORT'], int(os.environ['SCANNER_BAUDRATE']))

prevScan = None
while True:
  scan = myScanner.readNext()
  
  if(scan.status == 1 and (prevScan is None or scan.data != prevScan.data)):
    prevScan = scan
    print(scan)