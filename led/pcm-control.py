from RPi import GPIO
from pynput import keyboard

from mypylib.gpio import get_channel


channel = get_channel(2)

freq = 128  # pcm frequency
dc = 50  # duty cycle, control the voltage
dc_step, dc_max, dc_min = 10, 100, 0
dc_levels = int((dc_max - dc_min) / dc_step)
dc_values = [3.3 / dc_levels * i for i in range(0, dc_levels + 1)]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, freq)
p.start(100)


def on_press(key):
    global dc, dc_step, dc_max, dc_min
    if key == keyboard.Key.up:
        if dc + dc_step <= dc_max:
            dc += dc_step
            print(f"<voltage: {dc}%> increase voltage")
            p.ChangeDutyCycle(dc)
        else:
            print(f"<voltage: {dc}%> voltage has reached maximum")
    elif key == keyboard.Key.down:
        if dc - dc_step >= dc_min:
            dc -= dc_step
            print(f"<voltage: {dc}%> decrease voltage")
            p.ChangeDutyCycle(dc)
        else:
            print(f"<voltage: {dc}%> voltage has reached minimum")


def on_release(key):
    if key == keyboard.Key.esc:
        # stop listener
        return False


print("Runing on channel", channel)
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True,
) as listener:
    listener.join()

p.stop()
GPIO.cleanup()
print("Exit program")
