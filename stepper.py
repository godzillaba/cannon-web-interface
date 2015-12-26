import RPi.GPIO as GPIO
from datetime import datetime
import time

GPIO.setmode(GPIO.BOARD)

pins = {
    "x": {
        "pulse": 40,
        "direction": 38,
        "enable": 36
    }
}

for axis in pins:
    for pin in pins[axis]:
        GPIO.setup(pins[axis][pin], GPIO.OUT)
        GPIO.output(pins[axis][pin], True)

delay = .02
steps = 0

t1 = datetime.now()

while steps < 400:
    GPIO.output(pins['x']['pulse'], False)
    time.sleep(delay)
    GPIO.output(pins['x']['pulse'], True)
    time.sleep(delay)

    steps += 1

    print steps
t2 = datetime.now()

delta = t2-t1

dSeconds = delta.total_seconds()

rpm = 1/dSeconds * 60

print "RPM: " + str(rpm)
print "Delay: %s" % delay
print "\nRPM/Delay: %s" % (rpm/delay)

GPIO.output(pins['x']['enable'], False)