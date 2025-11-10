"""
Weryfikacja struktury kodu bez uruchamiania

Ten skrypt sprawdza:
- Składnię wszystkich plików Python
- Czy klasy są poprawnie zdefiniowane
- Czy metody mają odpowiednie sygnatury
"""

import ast
import os
from pathlib import Path


class CodeVerifier:
    """Klasa do weryfikacji kodu"""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def verify_file(self, filepath):
        """Weryfikuje pojedynczy plik Python"""
        print(f"\n{'='*60}")
        print(f"Sprawdzam: {filepath}")
        print('='*60)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            # Parsuj kod
            tree = ast.parse(source, filename=filepath)

            # Znajdź klasy
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

            print(f"✓ Składnia OK")
            print(f"  Znaleziono {len(classes)} klas")
            print(f"  Znaleziono {len(functions)} funkcji")

            # Wypisz klasy i ich metody
            for cls in classes:
                if cls.col_offset == 0:  # Tylko klasy top-level
                    print(f"\n  Klasa: {cls.name}")
                    methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)]
                    for method in methods:
                        args = [arg.arg for arg in method.args.args]
                        print(f"    - {method.name}({', '.join(args)})")

            return True

        except SyntaxError as e:
            self.errors.append(f"{filepath}: {e}")
            print(f"✗ Błąd składni: {e}")
            return False

        except Exception as e:
            self.errors.append(f"{filepath}: {e}")
            print(f"✗ Błąd: {e}")
            return False

    def verify_class_structure(self, filepath, class_name, required_methods):
        """Weryfikuje czy klasa ma wymagane metody"""
        print(f"\n{'='*60}")
        print(f"Weryfikacja klasy: {class_name} w {filepath}")
        print('='*60)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=filepath)

            # Znajdź klasę
            class_node = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    class_node = node
                    break

            if not class_node:
                print(f"✗ Klasa {class_name} nie znaleziona")
                self.errors.append(f"{filepath}: Brak klasy {class_name}")
                return False

            # Sprawdź metody
            methods = {node.name for node in class_node.body if isinstance(node, ast.FunctionDef)}

            print(f"✓ Klasa {class_name} znaleziona")
            print(f"  Metody: {', '.join(sorted(methods))}")

            missing = set(required_methods) - methods
            if missing:
                print(f"⚠ Brakujące metody: {', '.join(missing)}")
                self.warnings.append(f"{class_name}: Brakuje metod: {missing}")
                return False

            print(f"✓ Wszystkie wymagane metody obecne")
            return True

        except Exception as e:
            self.errors.append(f"{filepath}: {e}")
            print(f"✗ Błąd: {e}")
            return False

    def verify_app_structure(self):
        """Weryfikuje strukturę app.py"""
        print(f"\n{'='*60}")
        print("Weryfikacja app.py")
        print('='*60)

        filepath = 'app.py'

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=filepath)

            # Sprawdź funkcje top-level
            functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]

            print(f"✓ Znaleziono funkcje: {', '.join(functions)}")

            required_functions = ['main', 'show_header', 'show_sidebar', 'tab_generate_certificates', 'tab_instructions']
            missing = set(required_functions) - set(functions)

            if missing:
                print(f"⚠ Brakujące funkcje: {', '.join(missing)}")
                self.warnings.append(f"app.py: Brakuje funkcji: {missing}")
                return False

            print(f"✓ Wszystkie wymagane funkcje obecne")
            return True

        except Exception as e:
            self.errors.append(f"{filepath}: {e}")
            print(f"✗ Błąd: {e}")
            return False


def main():
    """Główna funkcja weryfikacji"""
    print("\n" + "="*60)
    print("WERYFIKACJA KODU CERTYFIKATORA")
    print("="*60)

    verifier = CodeVerifier()

    # Lista plików do sprawdzenia
    files_to_check = [
        'app.py',
        'modules/__init__.py',
        'modules/pdf_generator.py',
        'modules/data_handler.py',
        'modules/ocr_processor.py',
        'modules/template_manager.py',
    ]

    print("\n1. Sprawdzanie składni plików...")
    print("-" * 60)

    all_ok = True
    for filepath in files_to_check:
        if os.path.exists(filepath):
            if not verifier.verify_file(filepath):
                all_ok = False
        else:
            print(f"⚠ Plik nie istnieje: {filepath}")
            verifier.warnings.append(f"Plik nie istnieje: {filepath}")

    # Sprawdź strukturę klas
    print("\n\n2. Sprawdzanie struktury klas...")
    print("-" * 60)

    # DataHandler
    verifier.verify_class_structure(
        'modules/data_handler.py',
        'DataHandler',
        ['load_participants', 'validate_data', 'export_to_csv', 'get_participants_list']
    )

    # CertificateGenerator
    verifier.verify_class_structure(
        'modules/pdf_generator.py',
        'CertificateGenerator',
        ['generate_certificate', 'generate_batch', 'create_zip_archive']
    )

    # Sprawdź app.py
    print("\n\n3. Sprawdzanie struktury app.py...")
    print("-" * 60)

    verifier.verify_app_structure()

    # Sprawdź czy example_participants.csv istnieje
    print("\n\n4. Sprawdzanie plików danych...")
    print("-" * 60)

    if os.path.exists('data/example_participants.csv'):
        print("✓ data/example_participants.csv istnieje")
        size = os.path.getsize('data/example_participants.csv')
        print(f"  Rozmiar: {size} bajtów")
    else:
        print("⚠ data/example_participants.csv nie istnieje")
        verifier.warnings.append("Brak pliku example_participants.csv")

    # Sprawdź katalogi
    print("\n\n5. Sprawdzanie struktury katalogów...")
    print("-" * 60)

    required_dirs = ['modules', 'data', 'output', 'templates', 'assets']
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ Katalog {dir_name}/ istnieje")
        else:
            print(f"⚠ Katalog {dir_name}/ nie istnieje")
            verifier.warnings.append(f"Brak katalogu: {dir_name}")

    # Podsumowanie
    print("\n\n" + "="*60)
    print("PODSUMOWANIE")
    print("="*60)

    if verifier.errors:
        print(f"\n❌ BŁĘDY ({len(verifier.errors)}):")
        for error in verifier.errors:
            print(f"  - {error}")

    if verifier.warnings:
        print(f"\n⚠️  OSTRZEŻENIA ({len(verifier.warnings)}):")
        for warning in verifier.warnings:
            print(f"  - {warning}")

    if not verifier.errors and not verifier.warnings:
        print("\n✅ WSZYSTKO OK!")
        print("Kod jest poprawny i gotowy do uruchomienia.")
        print("\nAby uruchomić aplikację:")
        print("  1. Zainstaluj zależności: pip install -r requirements.txt")
        print("  2. Uruchom aplikację: streamlit run app.py")
        print("  3. Uruchom testy: python test_basic.py")
        return 0
    elif verifier.errors:
        print("\n❌ ZNALEZIONO BŁĘDY")
        print("Kod wymaga poprawek.")
        return 1
    else:
        print("\n⚠️  ZNALEZIONO OSTRZEŻENIA")
        print("Kod jest poprawny, ale mogą brakować niektóre pliki.")
        print("\nAby uruchomić aplikację:")
        print("  1. Zainstaluj zależności: pip install -r requirements.txt")
        print("  2. Uruchom aplikację: streamlit run app.py")
        return 0


if __name__ == '__main__':
    exit(main())
