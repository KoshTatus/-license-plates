import json
import os
from multiprocessing import freeze_support

import argparse
import cv2

from image_loader import load_images_from_path, load_image
from plate_detector import PlateDetector
from text_detection import recognize_text
from utils import put_text_with_russian

YOLO_MODEL_FILE = "../model/license_plates_model.pt"

def main(input_path: str, output_path: str):
    plate_detector = PlateDetector(YOLO_MODEL_FILE)

    if os.path.isfile(input_path):
        images = [(input_path, load_image(input_path))]
    else:
        images = load_images_from_path(input_path)

    for image_path, image in images:
        results = plate_detector.detect_plates(image)
        recognized_numbers = []
        box_coordinates = []

        for result in results:
            x1, y1, x2, y2 = result
            box_coordinates.append((x1, y1, x2 - x1, y2 - y1))
            license_plate = image[y1:y2, x1:x2]

            if license_plate.size == 0:
                continue

            text_from_plate = recognize_text(license_plate)

            if text_from_plate:
                recognized_numbers.append(text_from_plate)

            text_on_image = text_from_plate
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text_position = (x1, y1 - 40)
            image = put_text_with_russian(image, text_on_image, text_position)

        image_name = os.path.basename(image_path)
        image_name_without_ext = image_name[:image_name.rfind(".")]
        folder_path = f"{output_path}/{image_name_without_ext}"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        cv2.imwrite(f"{folder_path}/detected-{image_name}", image)

        json_data = [
            {
                "filename": image_name,
                "plates": [
                    {
                        "box": {
                            "x": coordinates[0],
                            "y": coordinates[1],
                            "width": coordinates[2],
                            "height": coordinates[3]
                        },
                        "text": text,
                    }
                    for text, coordinates in zip(recognized_numbers, box_coordinates)
                ]
            }
        ]

        with open(f"{folder_path}/detected.json", "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)


        print(f"Автомобильные номера на изображении: {image_path}")
        for number in recognized_numbers:
            print(number)



if __name__ == "__main__":
    freeze_support()

    parser = argparse.ArgumentParser(description="Обработка изображений для распознавания автомобильных номеров.")

    parser.add_argument(
        "input_path",
        type=str,
        help="Путь к директории с изображениями для обработки (обязательный параметр)."
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default="./",
        help="Путь для сохранения результатов (необязательный параметр, по умолчанию сохраняет в папку, из которой запускается скрипт)."
    )

    args = parser.parse_args()

    output_path = args.output_path

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        main(input_path=args.input_path, output_path=output_path)
    except Exception as e:
        print(str(e))