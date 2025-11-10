"""
Podstawowe testy jednostkowe dla Certyfikatora

Ten plik zawiera podstawowe testy dla:
- DataHandler.load_participants()
- CertificateGenerator.generate_certificate()
"""

import unittest
import os
import tempfile
import pandas as pd
from pathlib import Path

# Dodaj katalog główny do ścieżki
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_handler import DataHandler
from modules.pdf_generator import CertificateGenerator


class TestDataHandler(unittest.TestCase):
    """Testy dla klasy DataHandler"""

    def setUp(self):
        """Przygotowanie przed każdym testem"""
        self.handler = DataHandler()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Sprzątanie po każdym teście"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_load_participants_csv(self):
        """Test wczytywania danych z pliku CSV"""
        # Przygotuj testowy plik CSV
        test_csv = os.path.join(self.temp_dir, 'test.csv')
        test_data = """Imię,Nazwisko,Warsztat,Data,Email
Jan,Kowalski,Python,2025-01-15,jan@example.com
Anna,Nowak,Python,2025-01-15,anna@example.com
"""
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write(test_data)

        # Test wczytywania
        df = self.handler.load_participants(test_csv)

        self.assertIsNotNone(df, "DataFrame nie powinien być None")
        self.assertEqual(len(df), 2, "Powinno być 2 rekordy")
        self.assertIn('Imię', df.columns, "Brak kolumny Imię")
        self.assertIn('Nazwisko', df.columns, "Brak kolumny Nazwisko")
        self.assertEqual(df.iloc[0]['Imię'], 'Jan')
        self.assertEqual(df.iloc[1]['Nazwisko'], 'Nowak')

    def test_load_participants_missing_file(self):
        """Test wczytywania nieistniejącego pliku"""
        with self.assertRaises(FileNotFoundError):
            self.handler.load_participants('nieistniejacy_plik.csv')

    def test_load_participants_missing_columns(self):
        """Test wczytywania pliku bez wymaganych kolumn"""
        # Plik bez kolumny "Warsztat"
        test_csv = os.path.join(self.temp_dir, 'test_invalid.csv')
        test_data = """Imię,Nazwisko,Data
Jan,Kowalski,2025-01-15
"""
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write(test_data)

        with self.assertRaises(ValueError):
            self.handler.load_participants(test_csv)

    def test_validate_data_correct(self):
        """Test walidacji poprawnych danych"""
        # Przygotuj poprawne dane
        data = {
            'Imię': ['Jan', 'Anna'],
            'Nazwisko': ['Kowalski', 'Nowak'],
            'Warsztat': ['Python', 'Python'],
            'Data': ['2025-01-15', '2025-01-15']
        }
        df = pd.DataFrame(data)

        errors = self.handler.validate_data(df)

        self.assertEqual(len(errors), 0, "Nie powinno być błędów walidacji")

    def test_validate_data_empty_values(self):
        """Test walidacji danych z pustymi wartościami"""
        data = {
            'Imię': ['Jan', ''],
            'Nazwisko': ['Kowalski', 'Nowak'],
            'Warsztat': ['Python', 'Python'],
            'Data': ['2025-01-15', '2025-01-15']
        }
        df = pd.DataFrame(data)

        errors = self.handler.validate_data(df)

        self.assertGreater(len(errors), 0, "Powinny być błędy walidacji")
        # Sprawdź czy jest komunikat o pustych wartościach
        has_empty_error = any('pust' in error.lower() for error in errors)
        self.assertTrue(has_empty_error, "Powinien być błąd o pustych wartościach")

    def test_validate_data_duplicates(self):
        """Test walidacji danych z duplikatami"""
        data = {
            'Imię': ['Jan', 'Jan'],
            'Nazwisko': ['Kowalski', 'Kowalski'],
            'Warsztat': ['Python', 'Python'],
            'Data': ['2025-01-15', '2025-01-15']
        }
        df = pd.DataFrame(data)

        errors = self.handler.validate_data(df)

        self.assertGreater(len(errors), 0, "Powinny być błędy walidacji")
        # Sprawdź czy jest komunikat o duplikatach
        has_duplicate_error = any('duplikat' in error.lower() for error in errors)
        self.assertTrue(has_duplicate_error, "Powinien być błąd o duplikatach")

    def test_get_participants_list(self):
        """Test konwersji DataFrame do listy słowników"""
        data = {
            'Imię': ['Jan', 'Anna'],
            'Nazwisko': ['Kowalski', 'Nowak'],
            'Warsztat': ['Python', 'Java'],
            'Data': ['2025-01-15', '2025-01-20'],
            'Email': ['jan@test.com', 'anna@test.com']
        }
        df = pd.DataFrame(data)

        participants = self.handler.get_participants_list(df)

        self.assertEqual(len(participants), 2, "Powinno być 2 uczestników")
        self.assertIsInstance(participants[0], dict, "Element powinien być słownikiem")
        self.assertEqual(participants[0]['imie'], 'Jan')
        self.assertEqual(participants[1]['nazwisko'], 'Nowak')
        self.assertIn('warsztat', participants[0], "Powinien być klucz 'warsztat'")

    def test_export_to_csv(self):
        """Test eksportu do CSV"""
        data = {
            'Imię': ['Jan', 'Anna'],
            'Nazwisko': ['Kowalski', 'Nowak'],
            'Warsztat': ['Python', 'Python'],
            'Data': ['2025-01-15', '2025-01-15']
        }
        df = pd.DataFrame(data)

        output_path = os.path.join(self.temp_dir, 'output.csv')
        result = self.handler.export_to_csv(df, output_path)

        self.assertTrue(result, "Eksport powinien się udać")
        self.assertTrue(os.path.exists(output_path), "Plik powinien istnieć")

        # Sprawdź czy można wczytać z powrotem
        df_loaded = pd.read_csv(output_path)
        self.assertEqual(len(df_loaded), 2, "Powinno być 2 rekordy")

    def test_example_participants_file(self):
        """Test z prawdziwym plikiem example_participants.csv"""
        example_path = 'data/example_participants.csv'

        if not os.path.exists(example_path):
            self.skipTest(f"Plik {example_path} nie istnieje")

        df = self.handler.load_participants(example_path)

        self.assertIsNotNone(df, "DataFrame nie powinien być None")
        self.assertGreater(len(df), 0, "Powinien być co najmniej 1 rekord")
        self.assertIn('Imię', df.columns)
        self.assertIn('Nazwisko', df.columns)


class TestCertificateGenerator(unittest.TestCase):
    """Testy dla klasy CertificateGenerator"""

    def setUp(self):
        """Przygotowanie przed każdym testem"""
        self.temp_dir = tempfile.mkdtemp()

        # Sprawdź czy ReportLab jest dostępny
        try:
            self.generator = CertificateGenerator()
        except ImportError:
            self.skipTest("ReportLab nie jest zainstalowany")

    def tearDown(self):
        """Sprzątanie po każdym teście"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_generate_certificate_basic(self):
        """Test podstawowego generowania certyfikatu"""
        participant = {
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'warsztat': 'Python dla początkujących',
            'data': '2025-01-15'
        }

        output_path = os.path.join(self.temp_dir, 'test_certificate.pdf')
        result = self.generator.generate_certificate(participant, output_path)

        self.assertTrue(result, "Generowanie powinno się udać")
        self.assertTrue(os.path.exists(output_path), "Plik PDF powinien istnieć")
        self.assertGreater(os.path.getsize(output_path), 1000, "Plik PDF powinien mieć > 1KB")

    def test_generate_certificate_polish_characters(self):
        """Test generowania certyfikatu z polskimi znakami"""
        participant = {
            'imie': 'Łukasz',
            'nazwisko': 'Żółciński',
            'warsztat': 'Szkolenie z języka Python',
            'data': '15 stycznia 2025'
        }

        output_path = os.path.join(self.temp_dir, 'test_polish.pdf')
        result = self.generator.generate_certificate(participant, output_path)

        self.assertTrue(result, "Generowanie z polskimi znakami powinno się udać")
        self.assertTrue(os.path.exists(output_path), "Plik PDF powinien istnieć")

    def test_generate_certificate_long_workshop_name(self):
        """Test z długą nazwą warsztatu"""
        participant = {
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'warsztat': 'Zaawansowane programowanie w Pythonie z wykorzystaniem frameworków Django i Flask oraz baz danych',
            'data': '2025-01-15'
        }

        output_path = os.path.join(self.temp_dir, 'test_long.pdf')
        result = self.generator.generate_certificate(participant, output_path)

        self.assertTrue(result, "Generowanie z długą nazwą powinno się udać")
        self.assertTrue(os.path.exists(output_path), "Plik PDF powinien istnieć")

    def test_generate_certificate_with_logo(self):
        """Test generowania certyfikatu z logo (jeśli istnieje)"""
        logo_path = 'assets/logo.png'

        # Pomiń jeśli logo nie istnieje
        if not os.path.exists(logo_path):
            self.skipTest("Logo nie istnieje")

        generator_with_logo = CertificateGenerator(logo_path=logo_path)

        participant = {
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'warsztat': 'Python',
            'data': '2025-01-15'
        }

        output_path = os.path.join(self.temp_dir, 'test_with_logo.pdf')
        result = generator_with_logo.generate_certificate(participant, output_path)

        self.assertTrue(result, "Generowanie z logo powinno się udać")
        self.assertTrue(os.path.exists(output_path), "Plik PDF powinien istnieć")

    def test_generate_batch(self):
        """Test generowania wielu certyfikatów"""
        participants = [
            {'imie': 'Jan', 'nazwisko': 'Kowalski', 'warsztat': 'Python', 'data': '2025-01-15'},
            {'imie': 'Anna', 'nazwisko': 'Nowak', 'warsztat': 'Python', 'data': '2025-01-15'},
            {'imie': 'Piotr', 'nazwisko': 'Wiśniewski', 'warsztat': 'Python', 'data': '2025-01-15'}
        ]

        files, success, errors = self.generator.generate_batch(
            participants,
            self.temp_dir,
            show_progress=False
        )

        self.assertEqual(success, 3, "Powinno się udać 3 certyfikaty")
        self.assertEqual(errors, 0, "Nie powinno być błędów")
        self.assertEqual(len(files), 3, "Powinno być 3 pliki")

        # Sprawdź czy pliki istnieją
        for file_path in files:
            self.assertTrue(os.path.exists(file_path), f"Plik {file_path} powinien istnieć")

    def test_create_zip_archive(self):
        """Test tworzenia archiwum ZIP"""
        # Najpierw wygeneruj certyfikaty
        participants = [
            {'imie': 'Jan', 'nazwisko': 'Kowalski', 'warsztat': 'Python', 'data': '2025-01-15'},
            {'imie': 'Anna', 'nazwisko': 'Nowak', 'warsztat': 'Python', 'data': '2025-01-15'}
        ]

        files, _, _ = self.generator.generate_batch(
            participants,
            self.temp_dir,
            show_progress=False
        )

        # Utwórz archiwum
        zip_path = os.path.join(self.temp_dir, 'test_archive.zip')
        result = self.generator.create_zip_archive(files, zip_path)

        self.assertIsNotNone(result, "Tworzenie ZIP powinno się udać")
        self.assertTrue(os.path.exists(zip_path), "Archiwum ZIP powinno istnieć")
        self.assertGreater(os.path.getsize(zip_path), 1000, "Archiwum powinno mieć > 1KB")

        # Sprawdź zawartość ZIP
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            names = zipf.namelist()
            self.assertEqual(len(names), 2, "Powinno być 2 pliki w archiwum")


class TestIntegration(unittest.TestCase):
    """Testy integracyjne"""

    def setUp(self):
        """Przygotowanie przed każdym testem"""
        self.temp_dir = tempfile.mkdtemp()

        try:
            self.handler = DataHandler()
            self.generator = CertificateGenerator()
        except ImportError:
            self.skipTest("Brak wymaganych bibliotek")

    def tearDown(self):
        """Sprzątanie po każdym teście"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_full_workflow(self):
        """Test pełnego workflow: wczytanie CSV -> walidacja -> generowanie -> ZIP"""
        # 1. Utwórz testowy CSV
        test_csv = os.path.join(self.temp_dir, 'test_participants.csv')
        test_data = """Imię,Nazwisko,Warsztat,Data,Email
Jan,Kowalski,Python dla początkujących,2025-01-15,jan@example.com
Anna,Nowak,Python dla początkujących,2025-01-15,anna@example.com
"""
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write(test_data)

        # 2. Wczytaj dane
        df = self.handler.load_participants(test_csv)
        self.assertIsNotNone(df)

        # 3. Waliduj
        errors = self.handler.validate_data(df)
        self.assertEqual(len(errors), 0, "Nie powinno być błędów walidacji")

        # 4. Konwertuj do listy
        participants = self.handler.get_participants_list(df)
        self.assertEqual(len(participants), 2)

        # 5. Generuj certyfikaty
        files, success, errors_count = self.generator.generate_batch(
            participants,
            self.temp_dir,
            show_progress=False
        )

        self.assertEqual(success, 2, "Powinno się udać 2 certyfikaty")
        self.assertEqual(errors_count, 0, "Nie powinno być błędów")

        # 6. Utwórz ZIP
        zip_path = os.path.join(self.temp_dir, 'all_certificates.zip')
        result = self.generator.create_zip_archive(files, zip_path)

        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(zip_path))


def run_tests():
    """Uruchom wszystkie testy"""
    # Utwórz test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Dodaj testy
    suite.addTests(loader.loadTestsFromTestCase(TestDataHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestCertificateGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Podsumowanie
    print("\n" + "="*70)
    print("PODSUMOWANIE TESTÓW")
    print("="*70)
    print(f"Uruchomiono: {result.testsRun} testów")
    print(f"Sukces: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Błędy: {len(result.failures)}")
    print(f"Wyjątki: {len(result.errors)}")
    print(f"Pominięte: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✅ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        return 0
    else:
        print("\n❌ NIEKTÓRE TESTY NIE POWIODŁY SIĘ")
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    exit(exit_code)
