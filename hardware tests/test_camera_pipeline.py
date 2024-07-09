import gpiozero
from picamera2 import Picamera2, Preview
from datetime import datetime
import time
from signal import pause


mds = gpiozero.Button("BOARD"+str(12))

mode = 1

def switch_mode():
    global mode
    if mode == 2:
        mode = 1
        print("Now in Test Mode")
    else:
        mode = 2
        print("Now in Train Mode")


def take_picture(self):
    picam2 = Picamera2()
    picam2.start_preview(Preview.NULL)
    for x in range(5):
        if mode == 1:
            path = f"Desktop/img_py/test/{self.pin}_{datetime.now():%Y-%m-%d-%H-%M-%S.%f}.jpg"
        if mode == 2:
            path = f"Desktop/img_py/train/{self.pin}_{datetime.now():%Y-%m-%d-%H-%M-%S.%f}.jpg"
        picam2.start_and_capture_file(path)
        time.sleep(0.5)
    picam2.close()

btns = [16,18,22]

#16 -> grün 23
#18 -> blau 24
#22 -> gelb 25

btns = [gpiozero.Button("BOARD"+str(btn)) for btn in btns]

for btn in btns:
    btn.when_released = take_picture

mds.when_released = switch_mode

pause()