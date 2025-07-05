from ultralytics import YOLO
from numpy import ndarray

class PlateDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect_plates(self, image: ndarray) -> list:
        results = self.model(image)
        detected_plates = []

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                detected_plates.append((x1, y1, x2, y2))

        return detected_plates