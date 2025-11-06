"""
Test klasy CertificateGenerator - generowanie certyfikatów PDF z ReportLab
"""

import os
from modules.pdf_generator import CertificateGenerator


def test_single_certificate():
    """Test generowania pojedynczego certyfikatu"""
    print("\n" + "="*60)
    print("TEST 1: Generowanie pojedynczego certyfikatu")
    print("="*60)

    generator = CertificateGenerator()

    participant = {
        'imie': 'Jan',
        'nazwisko': 'Kowalski',
        'warsztat': 'Python dla początkujących',
        'data': '2025-01-15'
    }

    output_path = 'output/test_certyfikat_single.pdf'

    print(f"\nGenerowanie certyfikatu dla: {participant['imie']} {participant['nazwisko']}")

    success = generator.generate_certificate(participant, output_path)

    if success:
        print(f"✓ Certyfikat wygenerowany: {output_path}")
        return True
    else:
        print("✗ Błąd podczas generowania certyfikatu")
        return False


def test_batch_certificates():
    """Test generowania certyfikatów wsadowo"""
    print("\n" + "="*60)
    print("TEST 2: Generowanie certyfikatów wsadowo")
    print("="*60)

    generator = CertificateGenerator()

    participants = [
        {
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'warsztat': 'Python dla początkujących',
            'data': '2025-01-15'
        },
        {
            'imie': 'Anna',
            'nazwisko': 'Nowak',
            'warsztat': 'Python dla początkujących',
            'data': '2025-01-15'
        },
        {
            'imie': 'Piotr',
            'nazwisko': 'Wiśniewski',
            'warsztat': 'Python dla początkujących',
            'data': '2025-01-15'
        }
    ]

    print(f"\nGenerowanie {len(participants)} certyfikatów...\n")

    files, success, errors = generator.generate_batch(
        participants,
        'output',
        show_progress=True
    )

    print(f"\n✓ Sukces: {success}")
    print(f"✗ Błędy: {errors}")
    print(f"\nWygenerowane pliki:")
    for f in files:
        print(f"  - {os.path.basename(f)}")

    return len(files) == len(participants)


def test_certificate_with_polish_chars():
    """Test obsługi polskich znaków"""
    print("\n" + "="*60)
    print("TEST 3: Obsługa polskich znaków")
    print("="*60)

    generator = CertificateGenerator()

    participant = {
        'imie': 'Łukasz',
        'nazwisko': 'Żółciński',
        'warsztat': 'Szkolenie z Pythona - Część I: Podstawy języka',
        'data': '15 stycznia 2025'
    }

    output_path = 'output/test_certyfikat_polish.pdf'

    print(f"\nGenerowanie certyfikatu dla: {participant['imie']} {participant['nazwisko']}")
    print(f"Warsztat: {participant['warsztat']}")

    success = generator.generate_certificate(participant, output_path)

    if success:
        print(f"✓ Certyfikat z polskimi znakami wygenerowany: {output_path}")
        return True
    else:
        print("✗ Błąd podczas generowania certyfikatu")
        return False


def test_zip_archive():
    """Test tworzenia archiwum ZIP"""
    print("\n" + "="*60)
    print("TEST 4: Tworzenie archiwum ZIP")
    print("="*60)

    generator = CertificateGenerator()

    # Najpierw wygeneruj certyfikaty
    participants = [
        {'imie': 'Adam', 'nazwisko': 'Kowalski', 'warsztat': 'Python', 'data': '2025-01-15'},
        {'imie': 'Barbara', 'nazwisko': 'Nowak', 'warsztat': 'Python', 'data': '2025-01-15'},
        {'imie': 'Celina', 'nazwisko': 'Wiśniewska', 'warsztat': 'Python', 'data': '2025-01-15'}
    ]

    print("\nGenerowanie certyfikatów...\n")
    files, success, errors = generator.generate_batch(
        participants,
        'output',
        show_progress=True
    )

    # Teraz utwórz archiwum ZIP
    print("\n\nTworzenie archiwum ZIP...")
    zip_path = generator.create_zip_archive(files, 'output/test_certyfikaty.zip')

    if zip_path and os.path.exists(zip_path):
        file_size = os.path.getsize(zip_path) / 1024  # KB
        print(f"✓ Archiwum utworzone: {zip_path}")
        print(f"  Rozmiar: {file_size:.2f} KB")
        return True
    else:
        print("✗ Błąd podczas tworzenia archiwum")
        return False


def test_long_workshop_name():
    """Test długiej nazwy warsztatu"""
    print("\n" + "="*60)
    print("TEST 5: Długa nazwa warsztatu")
    print("="*60)

    generator = CertificateGenerator()

    participant = {
        'imie': 'Jan',
        'nazwisko': 'Kowalski',
        'warsztat': 'Zaawansowane programowanie w Pythonie z wykorzystaniem frameworków Django i Flask',
        'data': '2025-01-15'
    }

    output_path = 'output/test_certyfikat_long_name.pdf'

    print(f"\nGenerowanie certyfikatu z długą nazwą warsztatu:")
    print(f"'{participant['warsztat']}'")

    success = generator.generate_certificate(participant, output_path)

    if success:
        print(f"✓ Certyfikat wygenerowany: {output_path}")
        return True
    else:
        print("✗ Błąd podczas generowania certyfikatu")
        return False


def test_with_example_data():
    """Test z danymi z example_participants.csv"""
    print("\n" + "="*60)
    print("TEST 6: Generowanie z example_participants.csv")
    print("="*60)

    try:
        from modules.data_handler import DataHandler

        handler = DataHandler()
        df = handler.load_participants('data/example_participants.csv')

        print(f"Wczytano {len(df)} uczestników\n")

        participants = handler.get_participants_list(df)

        generator = CertificateGenerator()

        files, success, errors = generator.generate_batch(
            participants,
            'output',
            show_progress=True
        )

        print(f"\n✓ Sukces: {success}")
        print(f"✗ Błędy: {errors}")

        # Utwórz archiwum ZIP
        if files:
            print("\nTworzenie archiwum ZIP...")
            zip_path = generator.create_zip_archive(files, 'output/example_certyfikaty.zip')

        return success == len(participants)

    except Exception as e:
        print(f"✗ Błąd: {e}")
        return False


def run_all_tests():
    """Uruchom wszystkie testy"""
    print("\n" + "="*60)
    print("URUCHAMIANIE TESTÓW CERTIFICATE GENERATOR")
    print("="*60)

    # Upewnij się, że katalog output istnieje
    os.makedirs('output', exist_ok=True)

    tests = [
        ("Pojedynczy certyfikat", test_single_certificate),
        ("Certyfikaty wsadowo", test_batch_certificates),
        ("Polskie znaki", test_certificate_with_polish_chars),
        ("Archiwum ZIP", test_zip_archive),
        ("Długa nazwa warsztatu", test_long_workshop_name),
        ("Example participants", test_with_example_data)
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Błąd w teście '{name}': {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Podsumowanie
    print("\n" + "="*60)
    print("PODSUMOWANIE TESTÓW")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} testów zakończonych sukcesem")

    if passed == total:
        print("\n🎉 Wszystkie testy przeszły pomyślnie!")
    else:
        print(f"\n⚠ {total - passed} testów nie powiodło się")


if __name__ == "__main__":
    run_all_tests()
