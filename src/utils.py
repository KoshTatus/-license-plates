import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def put_text_with_russian(image, text, position, font_path = "arial.ttf", font_size = 30, color = (0, 255, 0)):
    """
    Функция для добавления текста с поддержкой кириллицы на изображение.
    """

    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)