import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#3,5 modes
#11,13,15 leds

#GPIO.setup(8,GPIO.IN)
#GPIO.setup(10,GPIO.IN)

GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)


for i in [11,13,15]:
	GPIO.output(i,True)
	time.sleep(1)
	GPIO.output(i, False)
	time.sleep(1)


#btns 16,18,22
GPIO.setup(16, GPIO.IN) #green
GPIO.setup(18, GPIO.IN) #blue
GPIO.setup(22, GPIO.IN) #yellow

try:
	while True: # Run forever
		if GPIO.input(16) == GPIO.HIGH:
        	print("green was pushed!")
		if GPIO.input(18) == GPIO.HIGH:
			print("blue was pushed!")
		if GPIO.input(22) == GPIO.HIGH:
			print("yellow was pushed!")
except KeyboardInterrupt:
	pass

GPIO.cleanup()

