"""
Przykładowe testy i użycie klasy DataHandler

Ten plik demonstruje jak korzystać z DataHandler oraz zawiera
proste testy funkcjonalności.
"""

from modules.data_handler import DataHandler
import pandas as pd
import os


def test_load_participants():
    """Test wczytywania danych uczestników"""
    print("\n" + "="*60)
    print("TEST 1: Wczytywanie danych uczestników")
    print("="*60)

    handler = DataHandler()

    try:
        # Wczytaj przykładowe dane
        df = handler.load_participants('data/example_participants.csv')
        print(f"✓ Wczytano {len(df)} rekordów")
        print(f"✓ Kolumny: {list(df.columns)}")
        print("\nPierwsze 3 rekordy:")
        print(df.head(3))
        return df

    except FileNotFoundError as e:
        print(f"✗ Błąd: {e}")
        return None
    except ValueError as e:
        print(f"✗ Błąd walidacji: {e}")
        return None
    except Exception as e:
        print(f"✗ Nieoczekiwany błąd: {e}")
        return None


def test_validate_data(df):
    """Test walidacji danych"""
    print("\n" + "="*60)
    print("TEST 2: Walidacja danych")
    print("="*60)

    handler = DataHandler()

    if df is None:
        print("✗ Brak danych do walidacji")
        return False

    errors = handler.validate_data(df)

    if errors:
        print("✗ Znaleziono błędy:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ Wszystkie dane są poprawne!")
        return True


def test_validate_data_with_errors():
    """Test walidacji danych z błędami"""
    print("\n" + "="*60)
    print("TEST 3: Walidacja danych z błędami")
    print("="*60)

    handler = DataHandler()

    # Stwórz DataFrame z błędami
    data = {
        'Imię': ['Jan', '', 'Piotr', 'Jan'],  # Pusta wartość w 2. wierszu, duplikat
        'Nazwisko': ['Kowalski', 'Nowak', 'Wiśniewski', 'Kowalski'],  # Duplikat
        'Warsztat': ['Python', 'Java', 'Python', 'Python'],
        'Data': ['2025-01-15', '2025-01-20', 'invalid-date', '2025-01-15'],  # Nieprawidłowa data
        'Email': ['jan@example.com', 'anna@example.com', 'invalid-email', 'jan@example.com']  # Nieprawidłowy email
    }

    df = pd.DataFrame(data)
    print("Dane testowe z błędami:")
    print(df)

    errors = handler.validate_data(df)

    print(f"\n✓ Znaleziono {len(errors)} problemów:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")

    return errors


def test_get_participants_list(df):
    """Test konwersji do listy słowników"""
    print("\n" + "="*60)
    print("TEST 4: Konwersja do listy słowników")
    print("="*60)

    handler = DataHandler()

    if df is None:
        print("✗ Brak danych do konwersji")
        return None

    # Test z domyślnym mapowaniem
    participants = handler.get_participants_list(df)
    print(f"✓ Przygotowano {len(participants)} uczestników")
    print("\nPierwszy uczestnik (domyślne mapowanie):")
    if participants:
        print(participants[0])

    # Test z własnym mapowaniem
    custom_mapping = {
        'Imię': 'first_name',
        'Nazwisko': 'last_name',
        'Email': 'email',
        'Warsztat': 'workshop',
        'Data': 'date'
    }

    participants_custom = handler.get_participants_list(df, custom_mapping)
    print("\nPierwszy uczestnik (własne mapowanie):")
    if participants_custom:
        print(participants_custom[0])

    return participants


def test_export_to_csv(df):
    """Test eksportu do CSV"""
    print("\n" + "="*60)
    print("TEST 5: Eksport do CSV")
    print("="*60)

    handler = DataHandler()

    if df is None:
        print("✗ Brak danych do eksportu")
        return False

    try:
        # Eksport bez usuwania duplikatów
        output_path_1 = 'output/test_export.csv'
        handler.export_to_csv(df, output_path_1)
        print(f"✓ Wyeksportowano dane do: {output_path_1}")

        # Eksport z usuwaniem duplikatów
        output_path_2 = 'output/test_export_unique.csv'
        handler.export_to_csv(df, output_path_2, remove_duplicates=True)
        print(f"✓ Wyeksportowano dane bez duplikatów do: {output_path_2}")

        return True

    except Exception as e:
        print(f"✗ Błąd podczas eksportu: {e}")
        return False


def test_remove_duplicates():
    """Test usuwania duplikatów"""
    print("\n" + "="*60)
    print("TEST 6: Usuwanie duplikatów")
    print("="*60)

    handler = DataHandler()

    # Stwórz DataFrame z duplikatami
    data = {
        'Imię': ['Jan', 'Anna', 'Jan', 'Piotr', 'Anna'],
        'Nazwisko': ['Kowalski', 'Nowak', 'Kowalski', 'Wiśniewski', 'Nowak'],
        'Warsztat': ['Python', 'Java', 'Python', 'Python', 'Java'],
        'Data': ['2025-01-15', '2025-01-20', '2025-01-15', '2025-01-20', '2025-01-20']
    }

    df = pd.DataFrame(data)
    print(f"Oryginalne dane ({len(df)} rekordów):")
    print(df)

    df_clean, removed_count = handler.remove_duplicates(df)
    print(f"\n✓ Usunięto {removed_count} duplikatów")
    print(f"✓ Pozostało {len(df_clean)} unikalnych rekordów:")
    print(df_clean)

    return df_clean


def test_filter_by_attendance():
    """Test filtrowania według listy obecności"""
    print("\n" + "="*60)
    print("TEST 7: Filtrowanie według listy obecności")
    print("="*60)

    handler = DataHandler()

    # Wczytaj wszystkich uczestników
    try:
        df = handler.load_participants('data/example_participants.csv')
        print(f"Wszyscy uczestnicy ({len(df)} osób):")
        print(df[['Imię', 'Nazwisko']])

        # Lista obecności (tylko niektórzy uczestniczy)
        attendance = [
            ('Jan', 'Kowalski'),
            ('Anna', 'Nowak')
        ]

        print(f"\nLista obecności: {attendance}")

        # Filtruj
        df_present = handler.filter_by_attendance(df, attendance)
        print(f"\n✓ Obecnych: {len(df_present)} osób:")
        print(df_present[['Imię', 'Nazwisko', 'Warsztat']])

        return df_present

    except Exception as e:
        print(f"✗ Błąd: {e}")
        return None


def demonstrate_workflow():
    """Demonstracja pełnego workflow"""
    print("\n" + "="*60)
    print("DEMONSTRACJA: Pełny workflow przetwarzania danych")
    print("="*60)

    handler = DataHandler()

    try:
        # Krok 1: Wczytanie
        print("\n1. Wczytywanie danych...")
        df = handler.load_participants('data/example_participants.csv')
        print(f"   ✓ Wczytano {len(df)} rekordów")

        # Krok 2: Walidacja
        print("\n2. Walidacja danych...")
        errors = handler.validate_data(df)
        if errors:
            print("   ⚠ Znaleziono błędy:")
            for error in errors:
                print(f"     - {error}")
        else:
            print("   ✓ Dane są poprawne")

        # Krok 3: Czyszczenie (usunięcie duplikatów)
        print("\n3. Czyszczenie danych...")
        df_clean, removed = handler.remove_duplicates(df)
        if removed > 0:
            print(f"   ✓ Usunięto {removed} duplikatów")
        else:
            print("   ✓ Brak duplikatów")

        # Krok 4: Konwersja
        print("\n4. Konwersja do formatu słowników...")
        participants = handler.get_participants_list(df_clean)
        print(f"   ✓ Przygotowano {len(participants)} uczestników")

        # Krok 5: Eksport
        print("\n5. Eksport przetworzonych danych...")
        handler.export_to_csv(df_clean, 'output/participants_processed.csv')
        print("   ✓ Wyeksportowano do output/participants_processed.csv")

        print("\n" + "="*60)
        print("WORKFLOW ZAKOŃCZONY POMYŚLNIE!")
        print("="*60)

        return participants

    except Exception as e:
        print(f"\n✗ Błąd podczas przetwarzania: {e}")
        return None


def run_all_tests():
    """Uruchom wszystkie testy"""
    print("\n" + "="*60)
    print("URUCHAMIANIE WSZYSTKICH TESTÓW")
    print("="*60)

    # Test 1: Wczytywanie
    df = test_load_participants()

    # Test 2: Walidacja (dane poprawne)
    test_validate_data(df)

    # Test 3: Walidacja (dane z błędami)
    test_validate_data_with_errors()

    # Test 4: Konwersja do listy
    test_get_participants_list(df)

    # Test 5: Eksport
    test_export_to_csv(df)

    # Test 6: Usuwanie duplikatów
    test_remove_duplicates()

    # Test 7: Filtrowanie według obecności
    test_filter_by_attendance()

    # Demonstracja workflow
    demonstrate_workflow()

    print("\n" + "="*60)
    print("WSZYSTKIE TESTY ZAKOŃCZONE")
    print("="*60)


if __name__ == "__main__":
    # Upewnij się, że katalog output istnieje
    os.makedirs('output', exist_ok=True)

    # Uruchom wszystkie testy
    run_all_tests()
