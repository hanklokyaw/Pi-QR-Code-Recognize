#!/usr/bin/python3

import time
import numpy as np
import cv2
from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode

# Initialize Picamera2
picam2 = Picamera2()

# Set the desired preview resolution
preview_width = 1280  # Set your desired width
preview_height = 720  # Set your desired height

# Create a preview configuration with a supported pixel format (use YUYV)
preview_config = picam2.create_preview_configuration(main={"format": 'YUYV', "size": (preview_width, preview_height)})

picam2.configure(preview_config)

# Start the preview
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(1)

# Set controls for camera
picam2.set_controls({"AfMode": 0, "LensPosition": 425})

# Initialize variables to store barcode values
first_barcode = None
second_barcode = None


# Function to process frame for barcode detection
def process_frame(frame):
    global first_barcode, second_barcode

    # Convert YUYV frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_YUYV)

    # Decode barcodes in the RGB frame
    decoded_objects = decode(rgb_frame)

    for obj in decoded_objects:
        barcode_data = obj.data.decode('utf-8')
        (x, y, w, h) = obj.rect

        # Draw a green rectangle around the detected barcode
        cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Store the first and second barcode values
        if first_barcode is None:
            first_barcode = barcode_data
            print(f"First barcode detected: {first_barcode}")
        elif second_barcode is None and barcode_data != first_barcode:
            second_barcode = barcode_data
            print(f"Second barcode detected: {second_barcode}")
            break  # Stop detecting after both barcodes are recognized

    return rgb_frame


try:
    while True:
        # Capture frame from the camera
        frame = picam2.capture_array()

        # Print the shape of the frame to debug
        print(f"Captured frame shape: {frame.shape}")

        # Process the frame for barcode detection
        processed_frame = process_frame(frame)

        # Display the processed frame using OpenCV
        cv2.imshow("Barcode Scanner", processed_frame)

        # Break the loop if both barcodes are detected
        if first_barcode is not None and second_barcode is not None:
            break

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the camera and close windows
    picam2.stop()
    cv2.destroyAllWindows()

# Print the detected barcode values
print(f"Final Barcodes Detected: First: {first_barcode}, Second: {second_barcode}")
