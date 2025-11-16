#!/usr/bin/env python3
"""
Demo skrypt dla klasy AttendanceOCR
Pokazuje jak używać zaawansowanego OCR do przetwarzania list obecności
"""

import os
import sys
from modules.ocr_processor import AttendanceOCR, AttendanceResult

print("=" * 70)
print("DEMO: AttendanceOCR - Przetwarzanie list obecności z checkboxami")
print("=" * 70)
print()

# Sprawdź czy wymagane biblioteki są zainstalowane
try:
    from modules.ocr_processor import OPENCV_AVAILABLE, TESSERACT_AVAILABLE, PDF2IMAGE_AVAILABLE

    print("Status bibliotek:")
    print(f"  ✓ Pytesseract: {'Zainstalowany' if TESSERACT_AVAILABLE else 'BRAK'}")
    print(f"  ✓ OpenCV:      {'Zainstalowany' if OPENCV_AVAILABLE else 'BRAK'}")
    print(f"  ✓ pdf2image:   {'Zainstalowany' if PDF2IMAGE_AVAILABLE else 'BRAK'}")
    print()

    if not all([OPENCV_AVAILABLE, TESSERACT_AVAILABLE]):
        print("⚠️  Brak wymaganych bibliotek!")
        print("   Zainstaluj: pip install opencv-python pytesseract pillow")
        sys.exit(1)

except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    sys.exit(1)

# Przykładowa lista uczestników
participant_list = [
    "Jan Kowalski",
    "Anna Nowak",
    "Piotr Wiśniewski",
    "Maria Wójcik",
    "Tomasz Kamiński",
    "Katarzyna Lewandowska",
    "Michał Dąbrowski",
    "Agnieszka Zielińska"
]

print("Lista oczekiwanych uczestników:")
for i, participant in enumerate(participant_list, 1):
    print(f"  {i}. {participant}")
print()

# Inicjalizacja AttendanceOCR
print("Inicjalizacja AttendanceOCR...")
try:
    ocr = AttendanceOCR()
    print("✓ AttendanceOCR zainicjalizowany pomyślnie")
    print()
except ImportError as e:
    print(f"❌ Błąd: {e}")
    sys.exit(1)

# Przykład 1: Demonstracja metod
print("=" * 70)
print("PRZYKŁAD 1: Demonstracja poszczególnych metod")
print("=" * 70)
print()

# Ponieważ nie mamy prawdziwego skanu listy obecności, pokażemy
# dokumentację i sposób użycia każdej metody

print("1. preprocess_image(image_path)")
print("   Przetwarza obraz przed OCR:")
print("   - Konwersja PDF do obrazu (jeśli PDF)")
print("   - Konwersja do grayscale")
print("   - Deskew (korekta obrotu)")
print("   - CLAHE (zwiększenie kontrastu)")
print("   - Bilateral filter (redukcja szumu)")
print("   - Binaryzacja adaptacyjna")
print()
print("   Przykład użycia:")
print("   >>> processed_img = ocr.preprocess_image('lista_obecnosci.jpg')")
print()

print("2. extract_text(image)")
print("   Wykonuje OCR na przetworzonym obrazie")
print("   - Używa Tesseract OCR")
print("   - Język: Polski + Angielski")
print("   - Tryb: --oem 3 --psm 6")
print()
print("   Przykład użycia:")
print("   >>> text = ocr.extract_text(processed_img)")
print()

print("3. detect_checkboxes(image_path)")
print("   Wykrywa zaznaczone checkboxy za pomocą OpenCV")
print("   - Znajduje kontury")
print("   - Filtruje po rozmiarze (15-50 px)")
print("   - Sprawdza aspect ratio (0.8-1.2)")
print("   - Oblicza wypełnienie (>20% = zaznaczony)")
print()
print("   Przykład użycia:")
print("   >>> checkboxes = ocr.detect_checkboxes('lista_obecnosci.jpg')")
print("   >>> # Zwraca: [(x, y, w, h), ...]")
print()

print("4. match_names_to_checkboxes(text, checkbox_positions, participant_list)")
print("   Dopasowuje nazwiska z OCR do zaznaczonych checkboxów")
print("   - Parsuje tekst OCR")
print("   - Porównuje z listą uczestników")
print("   - Oblicza confidence score (0.0-1.0)")
print("   - Sortuje checkboxy po pozycji Y")
print()
print("   Przykład użycia:")
print("   >>> matches = ocr.match_names_to_checkboxes(text, checkboxes, participant_list)")
print("   >>> # Zwraca: [{'name': 'Jan Kowalski', 'confidence': 0.95, ...}, ...]")
print()

print("5. process_attendance_sheet(image_path, participant_list)")
print("   🌟 GŁÓWNA METODA - łączy wszystkie kroki")
print("   - Przetwarza obraz")
print("   - Wykonuje OCR")
print("   - Wykrywa checkboxy")
print("   - Dopasowuje nazwiska")
print("   - Klasyfikuje wyniki (present/absent/unrecognized)")
print()
print("   Przykład użycia:")
print("   >>> result = ocr.process_attendance_sheet('lista.jpg', participant_list)")
print("   >>> print(f'Obecnych: {len(result.present)}')")
print("   >>> print(f'Nieobecnych: {len(result.absent)}')")
print("   >>> print(f'Nierozpoznanych: {len(result.unrecognized)}')")
print()

# Przykład 2: Symulacja wyniku
print("=" * 70)
print("PRZYKŁAD 2: Symulacja wyniku przetwarzania")
print("=" * 70)
print()

# Tworzymy symulowany wynik (w rzeczywistości byłby z OCR)
simulated_result = AttendanceResult(
    present=[
        {'name': 'Jan Kowalski', 'confidence': 0.95, 'detected_line': 'Jan Kowalski'},
        {'name': 'Anna Nowak', 'confidence': 0.92, 'detected_line': 'Anna Nowak'},
        {'name': 'Maria Wójcik', 'confidence': 0.88, 'detected_line': 'Maria Wojcik'},
        {'name': 'Tomasz Kamiński', 'confidence': 0.97, 'detected_line': 'Tomasz Kaminski'},
    ],
    absent=[
        'Piotr Wiśniewski',
        'Katarzyna Lewandowska',
        'Michał Dąbrowski',
        'Agnieszka Zielińska'
    ],
    unrecognized=[
        'Janusz Nieznany',
    ]
)

print("📊 WYNIKI PRZETWARZANIA:")
print()
print(f"✓ Obecni ({len(simulated_result.present)}):")
for p in simulated_result.present:
    print(f"   {p['name']:<25} (confidence: {p['confidence']:.0%})")
print()

print(f"✗ Nieobecni ({len(simulated_result.absent)}):")
for a in simulated_result.absent:
    print(f"   {a}")
print()

if simulated_result.unrecognized:
    print(f"? Nierozpoznani - wymagana weryfikacja ({len(simulated_result.unrecognized)}):")
    for u in simulated_result.unrecognized:
        print(f"   {u}")
    print()

# Przykład 3: Jak używać w praktyce
print("=" * 70)
print("PRZYKŁAD 3: Użycie w praktyce")
print("=" * 70)
print()

print("Krok po kroku - jak przetworzyć prawdziwą listę obecności:")
print()
print("1. Przygotuj skan listy obecności (JPG, PNG lub PDF)")
print("   - Upewnij się, że obraz jest dobrej jakości")
print("   - Checkboxy powinny być wyraźnie zaznaczone (X, ✓, lub zakreślone)")
print("   - Nazwiska powinny być czytelne")
print()
print("2. Przygotuj listę oczekiwanych uczestników")
print("   participants = ['Jan Kowalski', 'Anna Nowak', ...]")
print()
print("3. Utwórz instancję AttendanceOCR")
print("   ocr = AttendanceOCR()")
print()
print("4. Przetwórz listę obecności")
print("   result = ocr.process_attendance_sheet('scan.jpg', participants)")
print()
print("5. Analizuj wyniki")
print("   - result.present - lista obecnych (z confidence)")
print("   - result.absent - lista nieobecnych")
print("   - result.unrecognized - do ręcznej weryfikacji")
print()

print("=" * 70)
print("UWAGI I WSKAZÓWKI:")
print("=" * 70)
print()
print("• Tesseract OCR wymaga instalacji systemowej:")
print("  - Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-pol")
print("  - macOS: brew install tesseract tesseract-lang")
print("  - Windows: pobierz z https://github.com/UB-Mannheim/tesseract/wiki")
print()
print("• Jakość skanów ma kluczowe znaczenie:")
print("  - Preferowane: 300 DPI lub więcej")
print("  - Format: JPEG, PNG lub PDF")
print("  - Unikaj rozmazań i cieni")
print()
print("• Confidence score:")
print("  - ≥ 0.7: Wysokie zaufanie (automatycznie zaakceptowane)")
print("  - < 0.7: Niskie zaufanie (wymaga weryfikacji)")
print()
print("• Logowanie:")
print("  - Wszystkie operacje są szczegółowo logowane")
print("  - Poziom: INFO (można zmienić na DEBUG dla więcej szczegółów)")
print()

print("=" * 70)
print("✅ DEMO ZAKOŃCZONE")
print("=" * 70)
print()
print("Aby przetworzyć prawdziwą listę obecności:")
print("  python demo_attendance_ocr.py <ścieżka_do_skanu> <plik_z_uczestnikami>")
print()

# Jeśli podano argumenty wiersza poleceń, przetwórz prawdziwy plik
if len(sys.argv) >= 3:
    image_path = sys.argv[1]
    participants_file = sys.argv[2]

    if not os.path.exists(image_path):
        print(f"❌ Plik nie istnieje: {image_path}")
        sys.exit(1)

    if not os.path.exists(participants_file):
        print(f"❌ Plik nie istnieje: {participants_file}")
        sys.exit(1)

    # Wczytaj listę uczestników
    with open(participants_file, 'r', encoding='utf-8') as f:
        real_participants = [line.strip() for line in f if line.strip()]

    print("=" * 70)
    print("PRZETWARZANIE PRAWDZIWEJ LISTY OBECNOŚCI")
    print("=" * 70)
    print()
    print(f"Obraz: {image_path}")
    print(f"Uczestników: {len(real_participants)}")
    print()

    # Przetwórz
    result = ocr.process_attendance_sheet(image_path, real_participants)

    # Wyświetl wyniki
    print()
    print("=" * 70)
    print("WYNIKI")
    print("=" * 70)
    print()
    print(f"✓ Obecnych: {len(result.present)}")
    print(f"✗ Nieobecnych: {len(result.absent)}")
    print(f"? Nierozpoznanych: {len(result.unrecognized)}")
    print()
