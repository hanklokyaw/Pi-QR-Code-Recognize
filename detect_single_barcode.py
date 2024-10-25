#!/usr/bin/python3

import time
import numpy as np
import cv2
from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode


# Function to recognize a single barcode and return it
def recognize_barcode():
    # Initialize Picamera2
    picam2 = Picamera2()

    # Set the desired preview resolution
    preview_width = 1280  # Set your desired width
    preview_height = 720  # Set your desired height

    # Create a preview configuration with a supported pixel format (use YUYV)
    preview_config = picam2.create_preview_configuration(
        main={"format": 'YUYV', "size": (preview_width, preview_height)})
    picam2.configure(preview_config)

    # Start the camera
    picam2.start()
    time.sleep(1)  # Allow the camera to warm up

    # Set controls for camera
    picam2.set_controls({"AfMode": 2, "AfTrigger": 0})

    try:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert YUYV frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_YUYV)

        # Decode barcodes in the RGB frame
        decoded_objects = decode(rgb_frame)

        # If a barcode is detected, return it
        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            print(f"Barcode detected: {barcode_data}")
            return barcode_data

        # If no barcode is found, print message
        print("No barcode recognized")
        return None

    finally:
        # Clean up: stop the camera and release resources
        picam2.stop()
        cv2.destroyAllWindows()


# Example usage
recognized_barcode = recognize_barcode()
if recognized_barcode:
    print(f"Recognized Barcode: {recognized_barcode}")
else:
    print("No barcode was recognized.")
