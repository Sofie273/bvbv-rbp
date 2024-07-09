import gpiozero
import time
from signal import pause

#3,5 modes
#11,13,15 leds

#btns 16,18,22

leds = [11,13,15]

leds = [gpiozero.LED("BOARD"+str(led)) for led in leds]

for led in leds:
    print("trying to start LED",led)
    led.on()
    time.sleep(3)
    led.off()
    time.sleep(3)

btns = [16,18,22]

btns = [gpiozero.Button("BOARD"+str(btn)) for btn in btns]


btns[0].when_pressed = leds[0].on
btns[0].when_released = leds[0].off

btns[1].when_pressed = leds[1].on
btns[1].when_released = leds[1].off

btns[2].when_pressed = leds[2].on
btns[2].when_released = leds[2].off

pause()

