from PIL import Image

image = Image.open('./data/inputs/PHOTO-2024-08-19-14-42-31.jpg')

data = list(image.getdata())
image_without_exif = Image.new(image.mode, image.size)
image_without_exif.putdata(data)

rotated_image = image_without_exif.rotate(-90, expand=True)

rotated_image.save('./data/inputs/PHOTO-2024-08-19-14-42-31.jpg')

image.close()
rotated_image.close()
