"""
Moduł do przetwarzania OCR list obecności
"""

import pytesseract
from PIL import Image
import os


class OCRProcessor:
    """Klasa do przetwarzania OCR na skanach list obecności"""

    def __init__(self, tesseract_path=None):
        """
        Inicjalizacja procesora OCR

        Args:
            tesseract_path (str, optional): Ścieżka do Tesseract OCR
        """
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
