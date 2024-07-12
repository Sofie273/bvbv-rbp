from picamera2 import Picamera2, Preview

picam2 = Picamera2()

capture_config = picam2.create_still_configuration()

picam2.start_preview(Preview.NULL)

picam2.switch_mode_and_capture_file(capture_config,"img_py/new_image.jpg")
picam2.close()
