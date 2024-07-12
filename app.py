import tensorflow as tf 
import keras
import cv2
import os
import numpy as np
import gpiozero
from picamera2 import Picamera2, Preview
from datetime import datetime
from signal import pause
import time

print("tensorflow version: "+ tf.__version__)
print("keras version: ", keras.__version__)

print("Dependencies loaded. Trying to load model...")

#Load the Model 
chckpnt = os.listdir("model")[0]

model = keras.saving.load_model(f"model/{chckpnt}")

print("Loading model successful. Setting up GPIOS....")

#set up GPIO Pins

leds = [11,13,15]

leds = [gpiozero.LED("BOARD"+str(led)) for led in leds]

for led in leds:
    led.on()
    time.sleep(0.5)
    led.off()

btns = [16,18,22]

btns = [gpiozero.Button("BOARD"+str(btn)) for btn in btns]


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
    capture_config = picam2.create_still_configuration()
    picam2.start_preview(Preview.NULL)
    if mode == 1:
            path = f"img_py/test/{self.pin}_{datetime.now():%Y-%m-%d-%H-%M-%S.%f}.jpg"
            picam2.switch_mode_and_capture_file(capture_config,path)
    if mode == 2:
        for x in range(5):
            path = f"img_py/train/{self.pin}_{datetime.now():%Y-%m-%d-%H-%M-%S.%f}.jpg"
            picam2.switch_mode_and_capture_file(capture_config,path)
            time.sleep(0.5)
    picam2.close()
    predict_picture()

def output_led(pred):
    leds[pred].on()
    time.sleep(3)
    leds[pred].off()

def output_error():
    for x in range(3):
        leds[0].on()
        leds[1].on()
        leds[2].on()
        time.sleep(0.5)
        leds[0].off()
        leds[1].off()
        leds[2].off()
        time.sleep(0.5)

def predict_picture():
    most_recent_file = None
    most_recent_time = 0
    # iterate over the files in the directory using os.scandir
    for entry in os.scandir("img_py/test"):
        if entry.is_file():
            # get the modification time of the file using entry.stat().st_mtime_ns
            mod_time = entry.stat().st_mtime_ns
            if mod_time > most_recent_time:
                # update the most recent file and its modification time
                most_recent_file = entry.name
                most_recent_time = mod_time

    img = cv2.imread(f"img_py/test/{most_recent_file}")

    img = cv2.resize(img, (32, 32))
    
    confidences = model.predict(img.reshape(1, 32, 32, 3))

    pred = np.argmax(confidences)

    print(confidences)

    if confidences[0][pred] > 0.5:
        print(f"Predicted: {pred} with confidence {confidences[0][pred]}")
        output_led(int(pred))
    else:
        print(f"Can not predict this picture with confidence")
        output_error()


for btn in btns:
    btn.when_released = take_picture

mds.when_released = switch_mode

print("Waiting for Button press...")

pause()
