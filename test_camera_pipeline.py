import gpiozero
from picamera2 import PiCamera2, Preview
from datetime import datetime
from signal import pause

mds = [3,5]

mds = [gpiozero.Button("BOARD"+str(md)) for md in mds]

def take_picture():
    picam2 = PiCamera2()
    picam2.start_preview(Preview.NULL)
    picam2.start_and_capture_file("Desktop/img_py/{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg", num_files=3, delay=0.5)
    picam2.close()

btns = [16,18,22]

btns = [gpiozero.Button("BOARD"+str(btn)) for btn in btns]

for btn in btns:
    btn.when_pressed = take_picture
