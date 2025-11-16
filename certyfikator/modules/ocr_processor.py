"""
Moduł do przetwarzania OCR list obecności
"""

import os
import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Opcjonalny import pytesseract i PIL
try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("PIL/pytesseract nie jest zainstalowany")

# Opcjonalny import OpenCV
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logger.warning("OpenCV nie jest zainstalowany")

# Opcjonalny import pdf2image
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    logger.warning("pdf2image nie jest zainstalowany")


@dataclass
class AttendanceResult:
    """Wynik przetwarzania listy obecności"""
    present: List[Dict[str, any]]  # Lista obecnych (z confidence)
    absent: List[str]  # Lista nieobecnych
    unrecognized: List[str]  # Lista nierozpoznanych (do weryfikacji)


class OCRProcessor:
    """Klasa do przetwarzania OCR na skanach list obecności"""

    def __init__(self, tesseract_path=None):
        """
        Inicjalizacja procesora OCR

        Args:
            tesseract_path (str, optional): Ścieżka do Tesseract OCR

        Raises:
            ImportError: Jeśli pytesseract nie jest zainstalowany
        """
        if not TESSERACT_AVAILABLE:
            raise ImportError(
                "Pytesseract nie jest zainstalowany. "
                "Zainstaluj: pip install pytesseract"
            )

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def extract_text_from_image(self, image_path, lang='pol'):
        """
        Wyciąga tekst ze skanowanego obrazu

        Args:
            image_path (str): Ścieżka do pliku obrazu
            lang (str): Język OCR (domyślnie 'pol' dla polskiego)

        Returns:
            str: Wyekstrahowany tekst lub None w przypadku błędu
        """
        try:
            # Otwórz obraz
            image = Image.open(image_path)

            # Wykonaj OCR
            text = pytesseract.image_to_string(image, lang=lang)

            return text

        except Exception as e:
            print(f"Błąd podczas OCR: {e}")
            return None

    def extract_names_from_attendance(self, image_path):
        """
        Wyciąga imiona i nazwiska z listy obecności

        Args:
            image_path (str): Ścieżka do skanu listy obecności

        Returns:
            list: Lista krotek (imię, nazwisko) lub None w przypadku błędu
        """
        try:
            text = self.extract_text_from_image(image_path)

            if not text:
                return None

            # Przetwórz tekst - to jest uproszczona wersja
            # W prawdziwej implementacji należałoby dodać bardziej
            # zaawansowaną logikę parsowania
            lines = text.split('\n')
            names = []

            for line in lines:
                # Usuń puste linie i białe znaki
                line = line.strip()
                if not line:
                    continue

                # Proste wykrywanie par Imię Nazwisko
                parts = line.split()
                if len(parts) >= 2:
                    # Zakładamy format: Imię Nazwisko
                    imie = parts[0]
                    nazwisko = parts[1]
                    names.append((imie, nazwisko))

            return names

        except Exception as e:
            print(f"Błąd podczas przetwarzania listy obecności: {e}")
            return None

    def process_attendance_folder(self, folder_path):
        """
        Przetwarza wszystkie skany list obecności w folderze

        Args:
            folder_path (str): Ścieżka do folderu ze skanami

        Returns:
            dict: Słownik {nazwa_pliku: lista_imion_nazwisk}
        """
        results = {}

        if not os.path.exists(folder_path):
            return results

        # Obsługiwane rozszerzenia
        valid_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Sprawdź rozszerzenie
            _, ext = os.path.splitext(filename)
            if ext.lower() not in valid_extensions:
                continue

            # Przetwórz plik
            names = self.extract_names_from_attendance(file_path)
            if names:
                results[filename] = names

        return results


class AttendanceOCR:
    """
    Zaawansowana klasa do przetwarzania list obecności z checkboxami.
    Wykrywa zaznaczone pola i dopasowuje je do nazwisk uczestników.
    """

    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Inicjalizacja OCR engine dla języka polskiego

        Args:
            tesseract_path (str, optional): Ścieżka do wykonalnego Tesseract

        Raises:
            ImportError: Jeśli wymagane biblioteki nie są zainstalowane
        """
        if not TESSERACT_AVAILABLE:
            raise ImportError(
                "Pytesseract i PIL nie są zainstalowane. "
                "Zainstaluj: pip install pytesseract pillow"
            )

        if not OPENCV_AVAILABLE:
            raise ImportError(
                "OpenCV nie jest zainstalowany. "
                "Zainstaluj: pip install opencv-python"
            )

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        # Konfiguracja OCR dla języka polskiego
        self.ocr_config = '--oem 3 --psm 6'
        self.lang = 'pol+eng'

        logger.info("AttendanceOCR zainicjalizowany pomyślnie")

    def preprocess_image(self, image_path: str) -> Optional[Image.Image]:
        """
        Przetwarza obraz przed OCR: konwersja, kontrast, redukcja szumu, deskew

        Args:
            image_path (str): Ścieżka do obrazu

        Returns:
            Image.Image: Przetworzony obraz lub None w przypadku błędu
        """
        try:
            logger.info(f"Przetwarzanie obrazu: {image_path}")

            # Wczytaj obraz
            if image_path.lower().endswith('.pdf'):
                if not PDF2IMAGE_AVAILABLE:
                    logger.error("pdf2image nie jest zainstalowany")
                    return None

                logger.info("Konwersja PDF do obrazu...")
                images = convert_from_path(image_path, dpi=300)
                if not images:
                    logger.error("Nie można przekonwertować PDF")
                    return None
                image = images[0]  # Bierzemy pierwszą stronę
            else:
                image = Image.open(image_path)

            # Konwersja do RGB jeśli potrzebna
            if image.mode != 'RGB':
                logger.debug("Konwersja do RGB")
                image = image.convert('RGB')

            # Konwersja do numpy array dla OpenCV
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            # Konwersja do grayscale
            logger.debug("Konwersja do grayscale")
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Deskew (korekta obrotu)
            logger.debug("Deskew - korekta obrotu")
            coords = np.column_stack(np.where(gray > 0))
            if len(coords) > 0:
                angle = cv2.minAreaRect(coords)[-1]
                if angle < -45:
                    angle = -(90 + angle)
                else:
                    angle = -angle

                # Obróć obraz jeśli kąt > 0.5 stopnia
                if abs(angle) > 0.5:
                    (h, w) = gray.shape[:2]
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    gray = cv2.warpAffine(
                        gray, M, (w, h),
                        flags=cv2.INTER_CUBIC,
                        borderMode=cv2.BORDER_REPLICATE
                    )
                    logger.debug(f"Obrócono o {angle:.2f} stopni")

            # Zwiększenie kontrastu (CLAHE)
            logger.debug("Zwiększanie kontrastu (CLAHE)")
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)

            # Redukcja szumu (bilateral filter)
            logger.debug("Redukcja szumu")
            denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

            # Binaryzacja adaptacyjna
            logger.debug("Binaryzacja adaptacyjna")
            binary = cv2.adaptiveThreshold(
                denoised, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )

            # Konwersja z powrotem do PIL Image
            processed_image = Image.fromarray(binary)

            logger.info("Przetwarzanie obrazu zakończone pomyślnie")
            return processed_image

        except Exception as e:
            logger.error(f"Błąd podczas przetwarzania obrazu: {e}")
            return None

    def extract_text(self, image: Image.Image) -> Optional[str]:
        """
        Wykonuje OCR na przetworzonym obrazie

        Args:
            image (Image.Image): Przetworzony obraz

        Returns:
            str: Rozpoznany tekst lub None w przypadku błędu
        """
        try:
            logger.info("Wykonywanie OCR...")

            # Wykonaj OCR z konfiguracją dla polskiego
            text = pytesseract.image_to_string(
                image,
                lang=self.lang,
                config=self.ocr_config
            )

            logger.info(f"OCR zakończony, wykryto {len(text)} znaków")
            logger.debug(f"Tekst (pierwsze 200 znaków): {text[:200]}")

            return text

        except Exception as e:
            logger.error(f"Błąd podczas OCR: {e}")
            return None

    def detect_checkboxes(self, image_path: str) -> List[Tuple[int, int, int, int]]:
        """
        Wykrywa zaznaczone checkboxy (X, ✓, zakreślone) za pomocą OpenCV

        Args:
            image_path (str): Ścieżka do obrazu

        Returns:
            List[Tuple[int, int, int, int]]: Lista współrzędnych (x, y, w, h) checkboxów
        """
        try:
            logger.info("Wykrywanie checkboxów...")

            # Wczytaj obraz
            if image_path.lower().endswith('.pdf'):
                if not PDF2IMAGE_AVAILABLE:
                    logger.error("pdf2image nie jest zainstalowany")
                    return []
                images = convert_from_path(image_path, dpi=300)
                if not images:
                    return []
                pil_image = images[0]
                cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            else:
                cv_image = cv2.imread(image_path)

            if cv_image is None:
                logger.error(f"Nie można wczytać obrazu: {image_path}")
                return []

            # Konwersja do grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Binaryzacja
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

            # Znajdź kontury
            contours, _ = cv2.findContours(
                binary,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            checkboxes = []

            # Filtruj kontury do wykrycia checkboxów
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)

                # Filtruj po rozmiarze (checkboxy mają typowo 15-50 px)
                if 15 < w < 50 and 15 < h < 50:
                    # Sprawdź czy kształt jest kwadratowy
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        # Sprawdź czy checkbox jest zaznaczony
                        roi = binary[y:y+h, x:x+w]
                        filled_pixels = cv2.countNonZero(roi)
                        total_pixels = w * h
                        fill_ratio = filled_pixels / total_pixels

                        # Jeśli wypełnienie > 20%, uznajemy za zaznaczony
                        if fill_ratio > 0.2:
                            checkboxes.append((x, y, w, h))
                            logger.debug(
                                f"Checkbox znaleziony: ({x}, {y}) "
                                f"rozmiar: {w}x{h}, wypełnienie: {fill_ratio:.1%}"
                            )

            logger.info(f"Znaleziono {len(checkboxes)} zaznaczonych checkboxów")
            return checkboxes

        except Exception as e:
            logger.error(f"Błąd podczas wykrywania checkboxów: {e}")
            return []

    def match_names_to_checkboxes(
        self,
        text: str,
        checkbox_positions: List[Tuple[int, int, int, int]],
        participant_list: List[str]
    ) -> List[Dict[str, any]]:
        """
        Dopasowuje nazwiska z OCR do zaznaczonych checkboxów

        Args:
            text (str): Tekst z OCR
            checkbox_positions (List): Lista pozycji checkboxów
            participant_list (List[str]): Lista oczekiwanych uczestników

        Returns:
            List[Dict]: Lista obecnych uczestników z confidence score
        """
        try:
            logger.info("Dopasowywanie nazwisk do checkboxów...")

            # Parsuj tekst - wyciągnij potencjalne nazwiska
            lines = text.split('\n')
            detected_names = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Szukaj wzorców: nazwisko imię lub imię nazwisko
                words = line.split()
                if len(words) >= 2:
                    # Próbuj dopasować do listy uczestników
                    for participant in participant_list:
                        participant_lower = participant.lower()
                        line_lower = line.lower()

                        # Oblicz podobieństwo (prosta implementacja)
                        if participant_lower in line_lower or \
                           any(word.lower() in participant_lower for word in words):
                            # Znaleziono potencjalne dopasowanie
                            detected_names.append({
                                'name': participant,
                                'detected_line': line,
                                'confidence': self._calculate_confidence(
                                    participant, line
                                )
                            })
                            break

            # Jeśli mamy checkboxy, dopasuj nazwiska do nich
            if checkbox_positions:
                # Sortuj checkboxy po pozycji Y (od góry do dołu)
                sorted_checkboxes = sorted(checkbox_positions, key=lambda cb: cb[1])

                # Dopasuj do wykrytych nazwisk
                matches = []
                for i, checkbox in enumerate(sorted_checkboxes):
                    if i < len(detected_names):
                        match = detected_names[i].copy()
                        match['checkbox_position'] = checkbox
                        matches.append(match)
                        logger.debug(
                            f"Dopasowano: {match['name']} -> checkbox na ({checkbox[0]}, {checkbox[1]})"
                        )

                logger.info(f"Dopasowano {len(matches)} uczestników do checkboxów")
                return matches
            else:
                # Brak checkboxów - zwróć wszystkie wykryte nazwiska
                logger.info(f"Brak checkboxów, znaleziono {len(detected_names)} nazwisk")
                return detected_names

        except Exception as e:
            logger.error(f"Błąd podczas dopasowywania: {e}")
            return []

    def _calculate_confidence(self, expected: str, detected: str) -> float:
        """
        Oblicza confidence score dla dopasowania nazwiska

        Args:
            expected (str): Oczekiwane nazwisko
            detected (str): Wykryte nazwisko

        Returns:
            float: Confidence score (0.0 - 1.0)
        """
        expected_lower = expected.lower()
        detected_lower = detected.lower()

        # Dokładne dopasowanie
        if expected_lower == detected_lower:
            return 1.0

        # Sprawdź czy expected jest w detected
        if expected_lower in detected_lower:
            return 0.9

        # Sprawdź wspólne słowa
        expected_words = set(expected_lower.split())
        detected_words = set(detected_lower.split())
        common = expected_words & detected_words

        if common:
            return len(common) / max(len(expected_words), len(detected_words))

        # Brak dopasowania
        return 0.0

    def process_attendance_sheet(
        self,
        image_path: str,
        participant_list: List[str]
    ) -> AttendanceResult:
        """
        Główna metoda łącząca wszystkie kroki przetwarzania listy obecności

        Args:
            image_path (str): Ścieżka do skanu listy obecności (JPG, PNG, PDF)
            participant_list (List[str]): Lista oczekiwanych uczestników

        Returns:
            AttendanceResult: Wynik przetwarzania z listami: present, absent, unrecognized
        """
        try:
            logger.info("="*60)
            logger.info(f"Rozpoczęcie przetwarzania: {image_path}")
            logger.info(f"Oczekiwanych uczestników: {len(participant_list)}")
            logger.info("="*60)

            # Krok 1: Przetwórz obraz
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                logger.error("Nie udało się przetworzyć obrazu")
                return AttendanceResult(
                    present=[],
                    absent=participant_list,
                    unrecognized=[]
                )

            # Krok 2: Wykonaj OCR
            text = self.extract_text(processed_image)
            if not text:
                logger.error("OCR nie zwrócił tekstu")
                return AttendanceResult(
                    present=[],
                    absent=participant_list,
                    unrecognized=[]
                )

            # Krok 3: Wykryj checkboxy
            checkboxes = self.detect_checkboxes(image_path)

            # Krok 4: Dopasuj nazwiska do checkboxów
            matches = self.match_names_to_checkboxes(
                text, checkboxes, participant_list
            )

            # Krok 5: Sklasyfikuj wyniki
            present = []  # Wysokie confidence
            unrecognized = []  # Niskie confidence - do weryfikacji

            for match in matches:
                if match['confidence'] >= 0.7:
                    present.append(match)
                else:
                    unrecognized.append(match['detected_line'])

            # Znajdź nieobecnych
            present_names = {m['name'] for m in present}
            absent = [p for p in participant_list if p not in present_names]

            # Logowanie podsumowania
            logger.info("="*60)
            logger.info("PODSUMOWANIE PRZETWARZANIA")
            logger.info("="*60)
            logger.info(f"Obecni ({len(present)}):")
            for p in present:
                logger.info(f"  ✓ {p['name']} (confidence: {p['confidence']:.0%})")

            logger.info(f"\nNieobecni ({len(absent)}):")
            for a in absent:
                logger.info(f"  ✗ {a}")

            if unrecognized:
                logger.info(f"\nNierozpoznani - wymagana weryfikacja ({len(unrecognized)}):")
                for u in unrecognized:
                    logger.info(f"  ? {u}")

            logger.info("="*60)

            return AttendanceResult(
                present=present,
                absent=absent,
                unrecognized=unrecognized
            )

        except Exception as e:
            logger.error(f"Błąd podczas przetwarzania listy obecności: {e}")
            return AttendanceResult(
                present=[],
                absent=participant_list,
                unrecognized=[]
            )
