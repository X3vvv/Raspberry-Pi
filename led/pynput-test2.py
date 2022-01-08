import pynput

with pynput.keyboard.Events() as events:
    key_event = 0
    for event in events:
    #迭代用法。
        if key_event == 0:
            key_event = event
        if event.key == pynput.keyboard.Key.esc:
            break
        else:
            print(f"Received event {event}")
    
    key_event = event.get()
    #get用法。
    #可以提供一个实数作为最长等待时间（单位秒），超过这个时间没有事件，
    #就会报错。错误类型是queue模块的Empty，而非TimeoutError。

#判断事件情况：

if isinstance(key_event, pynput.keyboard.Events.Press):
    print('按下按键', end = '')
elif isinstance(key_event, pynput.keyboard.Events.Release):
    print('松开按键', end = '')

#判断按键：

#*这个事件的`key`属性*对应才是*Listener方法获得的按键`'key'`*。

try:
    print(key_event.key.name)
except AttributeError:
    #说明这个是普通按键。
    print(key_event.key.char)
else:
    #两种判断方式，第一种是我自创的，第二种是官网上的。
    if (key_event.key.name).startswith('ctrl'):
        #通过名称判断。
        print('发生了ctrl键事件。')
    elif key_event.key is pynput.keyboard.Key.esc:
        print('发生了esc键事件。')