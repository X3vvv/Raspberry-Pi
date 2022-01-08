# reference: https://zhuanlan.zhihu.com/p/73634679

import RPi.GPIO as GPIO
from time import sleep

outpin = 21
duration = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(outpin, GPIO.OUT)

try:
    print(f"Runing on GPIO<{outpin}>. Ctrl+C to stop.")
    for i in range(3):
        GPIO.output(outpin, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(outpin, GPIO.LOW)
        sleep(1)

except KeyboardInterrupt:
    print("Detected Ctrl+C, ending the program")

except:
    print("Error occurred")
    
finally:
    print("Clean up")
    GPIO.output(outpin, GPIO.LOW)
    GPIO.cleanup()
