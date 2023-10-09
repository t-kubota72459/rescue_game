import threading
import arduino
import time

BACKGROUND = False
th = None

def start():
    global BACKGROUND, th

    BACKGROUND = True
    th = threading.Thread(target=repeat, args=(6, ))
    th.start()

def repeat(num):
    while BACKGROUND:
        if not arduino.busy():
            arduino.play(num)
        time.sleep(1)

def cancel():
    global BACKGROUND, th

    if th is not None and th.is_alive():
        BACKGROUND = False
        th.join()
    th = None

def is_alive():
    if th is None:
        return False
    return th.is_alive()

if __name__ == '__main__':
    start()
    print("th:start")

    for _ in range(1):
        time.sleep(30)
        print(is_alive())

    print("th:cancel")
    cancel()

    print(is_alive())
    print(arduino.busy())
