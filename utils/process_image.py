from resize_image import detect_and_crop_head
from PIL import Image
import os
from process_exif import remove_exif 


def main(path):
    for f in os.listdir(path):
        file_name, file_format = os.path.splitext(f)
        file = file_name + file_format.lower()
        
        original_file = os.path.join(path, f)
        new_file = os.path.join(path, file)

        if f != file:
            os.rename(original_file, new_file)

        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            file_path = os.path.join(path, file)
            remove_exif(file_path)
            detect_and_crop_head(file_path, file_path)


if __name__ == "__main__":
    path = "../data/inputs"
    main(path)

