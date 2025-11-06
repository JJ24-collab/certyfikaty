#!/usr/bin/env python3
"""
Demonstracja użycia CertificateGenerator

Ten skrypt pokazuje jak używać klasy CertificateGenerator do generowania
profesjonalnych certyfikatów PDF z ReportLab.
"""

import os
from modules.pdf_generator import CertificateGenerator
from modules.data_handler import DataHandler


def demo_basic_usage():
    """Podstawowe użycie - generowanie pojedynczego certyfikatu"""
    print("\n" + "="*70)
    print("DEMO 1: Podstawowe użycie - pojedynczy certyfikat")
    print("="*70)

    # Krok 1: Inicjalizacja generatora
    print("\n1. Inicjalizacja generatora...")
    generator = CertificateGenerator()
    print("   ✓ Generator utworzony")

    # Krok 2: Przygotowanie danych uczestnika
    print("\n2. Przygotowanie danych uczestnika...")
    participant = {
        'imie': 'Jan',
        'nazwisko': 'Kowalski',
        'warsztat': 'Python dla początkujących',
        'data': '15 stycznia 2025'
    }
    print(f"   ✓ Uczestnik: {participant['imie']} {participant['nazwisko']}")
    print(f"   ✓ Warsztat: {participant['warsztat']}")

    # Krok 3: Generowanie certyfikatu
    print("\n3. Generowanie certyfikatu PDF...")
    output_path = 'output/demo_basic.pdf'
    success = generator.generate_certificate(participant, output_path)

    if success:
        print(f"   ✓ Certyfikat wygenerowany: {output_path}")
    else:
        print("   ✗ Błąd podczas generowania")


def demo_batch_generation():
    """Generowanie certyfikatów dla wielu uczestników"""
    print("\n" + "="*70)
    print("DEMO 2: Generowanie wsadowe - wiele certyfikatów")
    print("="*70)

    # Krok 1: Inicjalizacja
    print("\n1. Inicjalizacja generatora...")
    generator = CertificateGenerator()

    # Krok 2: Przygotowanie listy uczestników
    print("\n2. Przygotowanie listy uczestników...")
    participants = [
        {
            'imie': 'Anna',
            'nazwisko': 'Nowak',
            'warsztat': 'Python - poziom zaawansowany',
            'data': '20 stycznia 2025'
        },
        {
            'imie': 'Piotr',
            'nazwisko': 'Wiśniewski',
            'warsztat': 'Python - poziom zaawansowany',
            'data': '20 stycznia 2025'
        },
        {
            'imie': 'Maria',
            'nazwisko': 'Wójcik',
            'warsztat': 'Python - poziom zaawansowany',
            'data': '20 stycznia 2025'
        }
    ]
    print(f"   ✓ Przygotowano {len(participants)} uczestników")

    # Krok 3: Generowanie wsadowe
    print("\n3. Generowanie certyfikatów...\n")
    files, success, errors = generator.generate_batch(
        participants,
        'output',
        show_progress=True
    )

    print(f"\n   ✓ Wygenerowano: {success} certyfikatów")
    if errors > 0:
        print(f"   ✗ Błędy: {errors}")


def demo_with_csv_data():
    """Generowanie z danych z pliku CSV"""
    print("\n" + "="*70)
    print("DEMO 3: Generowanie z danych CSV")
    print("="*70)

    try:
        # Krok 1: Wczytanie danych z CSV
        print("\n1. Wczytywanie danych z CSV...")
        handler = DataHandler()
        df = handler.load_participants('data/example_participants.csv')
        print(f"   ✓ Wczytano {len(df)} uczestników")

        # Krok 2: Walidacja danych
        print("\n2. Walidacja danych...")
        errors = handler.validate_data(df)
        if errors:
            print("   ⚠ Ostrzeżenia:")
            for error in errors:
                print(f"     - {error}")
        else:
            print("   ✓ Dane są poprawne")

        # Krok 3: Konwersja do listy
        print("\n3. Przygotowanie listy uczestników...")
        participants = handler.get_participants_list(df)
        print(f"   ✓ Przygotowano {len(participants)} uczestników")

        # Krok 4: Generowanie certyfikatów
        print("\n4. Generowanie certyfikatów...\n")
        generator = CertificateGenerator()
        files, success, errors_count = generator.generate_batch(
            participants,
            'output',
            show_progress=True
        )

        print(f"\n   ✓ Wygenerowano: {success} certyfikatów")
        if errors_count > 0:
            print(f"   ✗ Błędy: {errors_count}")

    except Exception as e:
        print(f"\n   ✗ Błąd: {e}")


def demo_with_zip():
    """Generowanie certyfikatów i pakowanie do ZIP"""
    print("\n" + "="*70)
    print("DEMO 4: Generowanie + pakowanie do ZIP")
    print("="*70)

    # Krok 1: Przygotowanie danych
    print("\n1. Przygotowanie danych...")
    participants = [
        {'imie': 'Adam', 'nazwisko': 'Nowicki', 'warsztat': 'Django Framework', 'data': '2025-02-01'},
        {'imie': 'Barbara', 'nazwisko': 'Kowalska', 'warsztat': 'Django Framework', 'data': '2025-02-01'},
        {'imie': 'Celina', 'nazwisko': 'Kamińska', 'warsztat': 'Django Framework', 'data': '2025-02-01'}
    ]
    print(f"   ✓ Przygotowano {len(participants)} uczestników")

    # Krok 2: Generowanie certyfikatów
    print("\n2. Generowanie certyfikatów...\n")
    generator = CertificateGenerator()
    files, success, errors = generator.generate_batch(
        participants,
        'output',
        show_progress=True
    )

    # Krok 3: Tworzenie archiwum ZIP
    print("\n3. Tworzenie archiwum ZIP...")
    zip_path = generator.create_zip_archive(files, 'output/demo_certyfikaty.zip')

    if zip_path:
        file_size = os.path.getsize(zip_path) / 1024
        print(f"   ✓ Archiwum utworzone: {zip_path}")
        print(f"   ✓ Rozmiar: {file_size:.2f} KB")
        print(f"   ✓ Zawiera: {len(files)} certyfikatów")


def demo_polish_characters():
    """Demonstracja obsługi polskich znaków"""
    print("\n" + "="*70)
    print("DEMO 5: Obsługa polskich znaków")
    print("="*70)

    print("\n1. Generowanie certyfikatu z polskimi znakami...")

    generator = CertificateGenerator()

    participant = {
        'imie': 'Łukasz',
        'nazwisko': 'Żółciński',
        'warsztat': 'Programowanie w Pythonie - część I: Składnia języka',
        'data': '15 stycznia 2025 r.'
    }

    print(f"   Uczestnik: {participant['imie']} {participant['nazwisko']}")
    print(f"   Warsztat: {participant['warsztat']}")

    output_path = 'output/demo_polish.pdf'
    success = generator.generate_certificate(participant, output_path)

    if success:
        print(f"   ✓ Certyfikat wygenerowany: {output_path}")
    else:
        print("   ✗ Błąd podczas generowania")


def demo_with_logo():
    """Demonstracja certyfikatu z logo (jeśli istnieje)"""
    print("\n" + "="*70)
    print("DEMO 6: Certyfikat z logo organizacji")
    print("="*70)

    logo_path = 'assets/logo.png'

    print(f"\n1. Sprawdzanie dostępności logo...")
    if os.path.exists(logo_path):
        print(f"   ✓ Logo znalezione: {logo_path}")

        generator = CertificateGenerator(logo_path=logo_path)

        participant = {
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'warsztat': 'Python - warsztat praktyczny',
            'data': '2025-01-15'
        }

        print("\n2. Generowanie certyfikatu z logo...")
        output_path = 'output/demo_with_logo.pdf'
        success = generator.generate_certificate(participant, output_path)

        if success:
            print(f"   ✓ Certyfikat z logo wygenerowany: {output_path}")
        else:
            print("   ✗ Błąd podczas generowania")
    else:
        print(f"   ⚠ Logo nie znalezione: {logo_path}")
        print("   ℹ Aby dodać logo:")
        print("     1. Umieść plik PNG w lokalizacji: assets/logo.png")
        print("     2. Zalecany rozmiar: 400x400 pikseli")
        print("     3. Uruchom ponownie demo")


def main():
    """Uruchom wszystkie demonstracje"""
    print("\n" + "="*70)
    print("DEMONSTRACJA CERTIFICATE GENERATOR")
    print("Generowanie profesjonalnych certyfikatów PDF z ReportLab")
    print("="*70)

    # Upewnij się, że katalog output istnieje
    os.makedirs('output', exist_ok=True)
    print("\n✓ Katalog output przygotowany")

    # Uruchom wszystkie dema
    demos = [
        demo_basic_usage,
        demo_batch_generation,
        demo_with_csv_data,
        demo_with_zip,
        demo_polish_characters,
        demo_with_logo
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n✗ Błąd w demo: {e}")
            import traceback
            traceback.print_exc()

    # Podsumowanie
    print("\n" + "="*70)
    print("DEMONSTRACJA ZAKOŃCZONA")
    print("="*70)
    print("\nWygenerowane pliki znajdują się w katalogu: output/")
    print("\nPliki:")
    if os.path.exists('output'):
        files = [f for f in os.listdir('output') if f.endswith('.pdf') or f.endswith('.zip')]
        for f in sorted(files):
            file_path = os.path.join('output', f)
            size = os.path.getsize(file_path) / 1024
            print(f"  - {f} ({size:.1f} KB)")

    print("\n✨ Gotowe! Sprawdź wygenerowane certyfikaty.")


if __name__ == "__main__":
    main()
