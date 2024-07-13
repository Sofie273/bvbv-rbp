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
import timeit

print("tensorflow version: "+ tf.__version__)
print("keras version: ", keras.__version__)

class InferenceModel():
    """
    Class that makes it possible to load a checkpoint from a ".keras" checkpoint and use this model for inference
    """
    def __init__(self, checkpoint_path):
        self.hot_idx_to_label = ['bottle', 'can', 'cup']
        self.model = keras.saving.load_model(checkpoint_path)

    def predict(self, x, debug=False):
        # append a empty batch dimenstion if a single image is provided
        if len(x.shape) == 3:
            x = tf.expand_dims(x, axis=0)
            
        logits = self.model(x, training=False) #should be used instead of model.predict() for single samples
        logits = logits.numpy()
        pred_id = np.argmax(logits)
        confidence = logits[0][pred_id]
        pred_str = self.hot_idx_to_label[pred_id]

        # confidence threshold (at leased 20% more confident than random chance)
        random_chance = 1/len(logits[0])
        threshold = 1.2 * random_chance
        if confidence < threshold:
            pred_str = "background"
            output_error()
        if debug:
            print("predicted class '", pred_str, "' at index '", pred_id, "' from logits", logits)
            output_led(pred_id)

print("Dependencies loaded. Trying to load model...")

#Load the Model 
chckpnt = os.listdir("model")[0]

model = InferenceModel(f"model/{chckpnt}")
#model = keras.saving.load_model(f"model/{chckpnt}")

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
    picam2 = Picamera2(verbose_console=0)
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
    print("Timed:",timeit.timeit(lambda:predict_picture(), number=1))
    

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
    
    model.predict(img.reshape(1, 32, 32, 3), debug=True)


for btn in btns:
    btn.when_released = take_picture

mds.when_released = switch_mode

print("Waiting for Button press...")

pause()
