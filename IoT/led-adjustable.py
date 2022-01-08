import time
import RPi.GPIO as GPIO
import threading
from pynput import keyboard

stop_led_thread = False

channel = 21
pwm_freq = 30
pwm_freq_step = 20
pwm_freq_max, pwm_freq_min = 100, 10

blink_sleep_duration = 0.1
blink_sleep_duration_step = 0.02
blink_sleep_duration_max = 0.15  # decide min speed
blink_sleep_duration_min = 0.01  # decide max speed
blink_speed_total_level = (
    int(
        (blink_sleep_duration_max - blink_sleep_duration_min)
        // blink_sleep_duration_step
    )
    + 1
)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, pwm_freq)
p.start(0)


def pwmled():
    print("Start PWM led thread")
    try:
        while True:
            if stop_led_thread:
                break
            for dc in range(0, 100, 3):  # duty cycle: 0.0 <= dc <= 100.0
                if stop_led_thread:
                    break
                p.ChangeDutyCycle(dc)
                time.sleep(blink_sleep_duration)
            for dc in range(100, 0, -3):
                if stop_led_thread:
                    break
                p.ChangeDutyCycle(dc)
                time.sleep(blink_sleep_duration)

    except KeyboardInterrupt:
        print("Detected Ctrl+C, ending the program")

    except:
        print("Error occurred")

    finally:
        print("Clean up GPIO")
        p.stop()
        GPIO.cleanup()
    print("Exit pwm led thread")


def adjust():
    print("Start adjust thread")

    def press_handler(key):
        # print(f"pressed {key}")

        def adjust_freq(key):
            global pwm_freq, pwm_freq_step, pwm_freq_max, pwm_freq_min
            if key == keyboard.Key.up:
                if pwm_freq + pwm_freq_step > pwm_freq_max:
                    print(f"<{pwm_freq}Hz> PWM frequency has reached the maximum")
                else:
                    pwm_freq += pwm_freq_step
                    p.ChangeFrequency(pwm_freq)
                    print(f"<{pwm_freq}Hz> Increase PWM frequency")

            if key == keyboard.Key.down:
                if pwm_freq - pwm_freq_step < pwm_freq_min:
                    print(f"<{pwm_freq}Hz> PWM frequency has reached the minimum")
                else:
                    pwm_freq -= pwm_freq_step
                    p.ChangeFrequency(pwm_freq)
                    print(f"<{pwm_freq}Hz> Decrease PWM frequency")

        def adjust_speed(key):
            global blink_sleep_duration, blink_sleep_duration_step, blink_sleep_duration_max, blink_sleep_duration_min
            if (
                key == keyboard.Key.left
            ):  # lower speed ==> increase blink sleep duration
                if (
                    blink_sleep_duration + blink_sleep_duration_step
                    > blink_sleep_duration_max
                ):
                    print(
                        f"<Lv.{blink_speed_total_level - int((blink_sleep_duration - blink_sleep_duration_min) // blink_sleep_duration_step)}> blink speed has reached the minimum"
                    )
                else:
                    blink_sleep_duration += blink_sleep_duration_step
                    print(
                        f"<Lv.{blink_speed_total_level - int((blink_sleep_duration - blink_sleep_duration_min) // blink_sleep_duration_step)}> Decrease blink speed"
                    )

            if (
                key == keyboard.Key.right
            ):  # higher speed ==> decrease blink sleep duration
                if (
                    blink_sleep_duration - blink_sleep_duration_step
                    < blink_sleep_duration_min
                ):
                    print(
                        f"<Lv.{blink_speed_total_level - int((blink_sleep_duration - blink_sleep_duration_min) // blink_sleep_duration_step)}> blink speed has reached the maximum"
                    )
                else:
                    blink_sleep_duration -= blink_sleep_duration_step
                    print(
                        f"<Lv.{blink_speed_total_level - int((blink_sleep_duration - blink_sleep_duration_min) // blink_sleep_duration_step)}> Increase blink speed"
                    )

        try:
            key.char  # ignore non-special keys (arrow keys are special keys)
        except AttributeError:
            if key == keyboard.Key.up or key == keyboard.Key.down:
                adjust_freq(key)
            elif key == keyboard.Key.left or key == keyboard.Key.right:
                adjust_speed(key)

    def release_handler(key):
        # print(f"released {key}")
        if key == keyboard.Key.esc:
            # stop listener
            return False

    with keyboard.Listener(
        on_press=press_handler,
        on_release=release_handler,
        suppress=True,
    ) as listener:
        listener.join()

    print("Exit adjust thread")


led_thread = threading.Thread(target=pwmled)
adjust_thread = threading.Thread(target=adjust)

led_thread.start()
adjust_thread.start()

# Press will also Esc to stop PWM led thread
with keyboard.Events() as events:
    for one_event in events:
        if one_event.key is keyboard.Key.esc:
            stop_led_thread = True
            break

led_thread.join()
adjust_thread.join()

print("Exit program")
