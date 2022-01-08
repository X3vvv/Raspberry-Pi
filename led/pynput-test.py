# reference: https://www.cnblogs.com/tobe-goodlearner/p/tutorial-pynput.html
from pynput import keyboard

def on_press(key):
    '按下按键时执行。'
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
    #通过属性判断按键类型

def on_release(key):
    '松开按键时执行。'
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
# listener.start() and listener.stop() can be used to replace with keyboard.Listener()
print("Detect what u have pressed. Press `Esc` to exit")
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
