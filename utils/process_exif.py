from PIL import Image, ExifTags
import os


def remove_exif(path):
    image = Image.open(path)
    exif_data = image.getexif()
    if exif_data:
        print(f"Detected exif_data in {os.path.basename(path)}")
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        rotated_image = image_without_exif.rotate(-90, expand=True)
        rotated_image.save(path)
        image.close()
        rotated_image.close()
        return 
    else:
        print(f"Image not affected - did not detect exif data in {os.path.basename(path)}")
        return 


if __name__ == "__main__":
    main(path)







