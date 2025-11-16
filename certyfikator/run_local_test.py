#!/usr/bin/env python3
"""
Lokalny test aplikacji bez Streamlit
Testuje podstawowe funkcje modułów
"""

import sys
import os

print("="*70)
print("TEST LOKALNY - CERTYFIKATOR")
print("="*70)

# Test 1: Import modułów
print("\n1. Test importu modułów...")
print("-"*70)

try:
    # Dodaj katalog do ścieżki
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from modules.data_handler import DataHandler
    print("✓ DataHandler zaimportowany")

    try:
        from modules.pdf_generator import CertificateGenerator
        print("✓ CertificateGenerator zaimportowany")
        reportlab_available = True
    except ImportError as e:
        print(f"⚠ CertificateGenerator niedostępny: {e}")
        print("  (ReportLab nie jest zainstalowany)")
        reportlab_available = False

except Exception as e:
    print(f"✗ Błąd importu: {e}")
    sys.exit(1)

# Test 2: DataHandler
print("\n2. Test DataHandler...")
print("-"*70)

try:
    handler = DataHandler()
    print("✓ DataHandler utworzony")

    # Wczytaj example_participants.csv
    csv_path = 'data/example_participants.csv'
    if os.path.exists(csv_path):
        df = handler.load_participants(csv_path)
        print(f"✓ Wczytano {len(df)} rekordów z {csv_path}")
        print(f"  Kolumny: {list(df.columns)}")

        # Walidacja
        errors = handler.validate_data(df)
        if errors:
            print(f"⚠ Walidacja znalazła {len(errors)} problemów:")
            for error in errors[:3]:  # Pokaż pierwsze 3
                print(f"    - {error}")
        else:
            print("✓ Walidacja - dane poprawne")

        # Konwersja do listy
        participants = handler.get_participants_list(df)
        print(f"✓ Skonwertowano do {len(participants)} słowników")

        if participants:
            print(f"\n  Przykładowy uczestnik:")
            p = participants[0]
            print(f"    Imię: {p.get('imie')}")
            print(f"    Nazwisko: {p.get('nazwisko')}")
            print(f"    Warsztat: {p.get('warsztat')}")
            print(f"    Data: {p.get('data')}")
    else:
        print(f"⚠ Plik {csv_path} nie istnieje")

except Exception as e:
    print(f"✗ Błąd w DataHandler: {e}")
    import traceback
    traceback.print_exc()

# Test 3: CertificateGenerator
if reportlab_available:
    print("\n3. Test CertificateGenerator...")
    print("-"*70)

    try:
        generator = CertificateGenerator()
        print("✓ CertificateGenerator utworzony")

        # Przygotuj dane testowe
        test_participant = {
            'imie': 'Jan',
            'nazwisko': 'Testowy',
            'warsztat': 'Test Lokalny',
            'data': '2025-11-16'
        }

        # Generuj certyfikat
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'test_lokalny.pdf')

        print(f"  Generowanie certyfikatu dla: {test_participant['imie']} {test_participant['nazwisko']}")

        result = generator.generate_certificate(test_participant, output_path)

        if result and os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ Certyfikat wygenerowany: {output_path}")
            print(f"  Rozmiar: {size} bajtów ({size/1024:.1f} KB)")
        else:
            print(f"✗ Nie udało się wygenerować certyfikatu")

    except Exception as e:
        print(f"✗ Błąd w CertificateGenerator: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n3. Test CertificateGenerator...")
    print("-"*70)
    print("⚠ Pominięto - ReportLab nie jest zainstalowany")

# Test 4: Sprawdź strukturę projektu
print("\n4. Sprawdzenie struktury projektu...")
print("-"*70)

required_files = [
    'app.py',
    'modules/__init__.py',
    'modules/data_handler.py',
    'modules/pdf_generator.py',
    'data/example_participants.csv',
    'README.md',
    'QUICKSTART.md',
    'requirements.txt'
]

all_exist = True
for filepath in required_files:
    if os.path.exists(filepath):
        print(f"✓ {filepath}")
    else:
        print(f"✗ {filepath} - brak")
        all_exist = False

required_dirs = ['modules', 'data', 'output', 'templates', 'assets']
for dirname in required_dirs:
    if os.path.isdir(dirname):
        print(f"✓ {dirname}/")
    else:
        print(f"✗ {dirname}/ - brak")
        all_exist = False

# Podsumowanie
print("\n" + "="*70)
print("PODSUMOWANIE")
print("="*70)

if all_exist:
    print("\n✅ Wszystkie pliki i katalogi na miejscu")
else:
    print("\n⚠ Brakuje niektórych plików lub katalogów")

if reportlab_available:
    print("✅ ReportLab dostępny - generowanie PDF działa")
else:
    print("⚠ ReportLab niedostępny - zainstaluj: pip install reportlab")

print("\n📝 Aby uruchomić pełną aplikację Streamlit:")
print("   1. pip install -r requirements.txt")
print("   2. streamlit run app.py")
print("\n📝 Aby uruchomić testy:")
print("   python test_basic.py")
print("\n" + "="*70)
