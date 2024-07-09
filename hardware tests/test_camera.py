from picamera2 import Picamera2, Preview

picam2 = Picamera2()

picam2.start_preview(Preview.NULL)

#Verzeichnis muss vorher angelegt werden!
picam2.start_and_capture_file("Desktop/img_py/new_image.jpg")
picam2.close()