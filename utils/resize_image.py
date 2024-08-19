# Code taken from https://gist.github.com/Norod/223b81b7131cec3ac21cf3be3e47a597

import cv2
import numpy as np
from PIL import Image

def detect_and_crop_head(input_img_path, output_image_path, factor=1.7, target_resolution=(1024, 1024)):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    image = Image.open(input_img_path)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = faces[0]

        center_x = x + w // 2
        center_y = y + h // 2
        size = int(max(w,h) * factor)
        x_new = max(0, center_x - size // 2)
        y_new = max(0, center_y - size // 2)

        x_new_end = min(cv_image.shape[1], x_new + size)
        y_new_end = min(cv_image.shape[0], y_new + size)

        cropped_head = cv_image[y_new:y_new_end, x_new:x_new_end]
        resized_head = cv2.resize(cropped_head, target_resolution)

        resized_head_pil = Image.fromarray(cv2.cvtColor(resized_head, cv2.COLOR_BGR2RGB))
        resized_head_pil.save(output_image_path)
        print("Cropped and resized head saved successfully")
    else:
        print("No faces detected in the input image.")


if __name__ == "__main__":
    input_img_path = './data/inputs/PHOTO-2024-08-19-14-42-31.jpg'
    output_img_path = './data/inputs/PHOTO-2024-08-19-14-42-31.jpg'
    detect_and_crop_head(input_img_path, output_img_path)