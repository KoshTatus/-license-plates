import cv2
import pytesseract

PLATE_SYMBOLS = "АВСЕКМОРНТУХ1234567890"

def filter_license_plate(license_plate: str) -> str:
    """
    Обработка символов в обнаруженном тексте.
    1. Замена буквы 'б' на цифру 6.
    2. Приведение всех символов к верхнему регистру
    3. Отсеивание символов, которые не используются в автомобильных номерах.

    """
    filtered_text = license_plate.replace("б", "6")
    filtered_text = filtered_text.upper()

    cleaned_text = ""

    for symbol in filtered_text:
        if symbol in PLATE_SYMBOLS:
            cleaned_text += symbol

    return cleaned_text

def preprocess_plate(image):
    """
    Предварительная обработка изображения номерного знака для улучшения качества распознавания.
    1. Изображение преобразуется в градации серого.
    2. Контрастность улучшается с помощью CLAHE.
    3. Шум устраняется с помощью Гауссова размытия.
    4. Изображение становится бинарным, что упрощает дальнейший анализ.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    normalized = clahe.apply(gray)
    blurred = cv2.GaussianBlur(normalized, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary

def recognize_text(image) -> str | None:
    processed_plate = preprocess_plate(image)
    ocr_result = pytesseract.image_to_string(processed_plate, lang='rus', config='--psm 8')

    filtered_text = filter_license_plate(ocr_result)

    return filtered_text


