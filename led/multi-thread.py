import threading
import time
import random

def hello(n):
    time.sleep(random.randint(1, 3))
    mylist.append(threading.get_ident())  # bad manner: append isnt thread-safe
    print(f"Thread-[{n}] Hello!")

mylist = []
threads = []
for i in range(10):
    t = threading.Thread(target=hello, args=(i,))
    threads.append(t)
    t.start()

for one_thread in threads:
    one_thread.join()

print("Done!")
print(mylist, f"- {len(mylist)} ids")