import RPi.GPIO as GPIO
from time import sleep

outpin = 21
freq = 1000 # PWM frequency
looptime = 100

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(outpin, GPIO.OUT)

pwm = GPIO.PWM(outpin, freq)
pwm.start(0) # start PWM

try:
    print(f"Runing {looptime} times on GPIO<{outpin}>, frequency = {freq}Hz.\nPress Ctrl+C to stop.")
    for i in range(looptime):
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            sleep(0.1)
        for dc in range(100, -1, -5):
            pwm.ChangeDutyCycle(dc)
            sleep(0.1)
        print(".", end="")

except KeyboardInterrupt:
    print("Detected Ctrl+C, ending the program")

except:
    print("Error occurred")
    
finally:
    print("Clean up")
    pwm.stop()
    GPIO.cleanup()
