import cv2
import os


def is_file_image(filename: str) -> bool:
    allowed_extensions = ('jpg', 'jpeg', 'png')
    return filename.endswith(allowed_extensions)

def load_image(image_path: str):
    try:
        if is_file_image(image_path):
            image = cv2.imread(image_path)
            return image
        return None

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {image_path}")

def load_images_from_path(images_path: str):
    if not os.path.exists(images_path):
        raise FileNotFoundError(f"Invalid path: {images_path}")

    images = []
    for image_path in os.listdir(images_path):
        image_path  = os.path.join(images_path, image_path)
        image = load_image(image_path)
        if image is not None:
            images.append((image_path, image))
    return images