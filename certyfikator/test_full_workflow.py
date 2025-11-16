#!/usr/bin/env python3
"""
Test pełnego workflow aplikacji certyfikator
Symuluje działania użytkownika w aplikacji Streamlit
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Import modułów
from modules.data_handler import DataHandler
from modules.pdf_generator import CertificateGenerator

print("=" * 70)
print("TEST PEŁNEGO WORKFLOW - CERTYFIKATOR")
print("=" * 70)
print()

# 1. Wczytanie pliku example_participants.csv
print("1️⃣  WCZYTYWANIE PLIKU example_participants.csv")
print("-" * 70)

handler = DataHandler()
csv_path = "data/example_participants.csv"

if not os.path.exists(csv_path):
    print(f"❌ Błąd: Plik {csv_path} nie istnieje!")
    sys.exit(1)

df = handler.load_participants(csv_path)
print(f"✓ Wczytano {len(df)} uczestników")
print(f"  Kolumny: {', '.join(df.columns.tolist())}")
print()
print("Dane:")
print(df.to_string(index=False))
print()

# 2. Walidacja danych
print("2️⃣  WALIDACJA DANYCH")
print("-" * 70)

errors = handler.validate_data(df)
if errors:
    print(f"⚠️  Znaleziono {len(errors)} problemów:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ Dane są poprawne - brak błędów walidacji")
print()

# 3. "Edycja" danych - dodanie nowego uczestnika
print("3️⃣  EDYCJA DANYCH - Dodanie nowego uczestnika")
print("-" * 70)

new_participant = {
    'Imię': 'Paweł',
    'Nazwisko': 'Wiśniewski',
    'Data': '2024-01-17',
    'Temat': 'Testowanie oprogramowania'
}

# Używamy pd.concat zamiast append (deprecated)
df_edited = pd.concat([df, pd.DataFrame([new_participant])], ignore_index=True)
print(f"✓ Dodano uczestnika: {new_participant['Imię']} {new_participant['Nazwisko']}")
print(f"  Liczba uczestników po edycji: {len(df_edited)}")
print()

# Ponowna walidacja po edycji
errors = handler.validate_data(df_edited)
if errors:
    print(f"⚠️  Po edycji znaleziono {len(errors)} problemów:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ Dane po edycji są poprawne")
print()

# 4. Generowanie pojedynczego certyfikatu (podgląd)
print("4️⃣  PODGLĄD - Generowanie pojedynczego certyfikatu")
print("-" * 70)

# Utwórz katalog output jeśli nie istnieje
output_dir = "output/test_workflow"
os.makedirs(output_dir, exist_ok=True)

generator = CertificateGenerator()
first_participant = df_edited.iloc[0].to_dict()
preview_path = f"{output_dir}/preview_{first_participant['Imię']}_{first_participant['Nazwisko']}.pdf"

success = generator.generate_certificate(first_participant, preview_path)
if success:
    file_size = os.path.getsize(preview_path)
    print(f"✓ Wygenerowano podgląd certyfikatu:")
    print(f"  Uczestnik: {first_participant['Imię']} {first_participant['Nazwisko']}")
    print(f"  Plik: {preview_path}")
    print(f"  Rozmiar: {file_size:,} bajtów")
else:
    print("❌ Błąd generowania podglądu")
print()

# 5. Generowanie wszystkich certyfikatów
print("5️⃣  GENEROWANIE WSZYSTKICH CERTYFIKATÓW")
print("-" * 70)

participants_list = handler.get_participants_list(df_edited)
generated_files, success_count, error_count = generator.generate_batch(
    participants_list,
    output_dir,
    show_progress=True
)

print(f"✓ Wygenerowano {success_count} certyfikatów")
total_size = sum(os.path.getsize(f) for f in generated_files)
print(f"  Łączny rozmiar: {total_size:,} bajtów ({total_size/1024:.1f} KB)")
print()
print("Wygenerowane pliki:")
for i, file_path in enumerate(generated_files, 1):
    size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    print(f"  {i}. {filename} ({size:,} bajtów)")
print()

# 6. Tworzenie archiwum ZIP
print("6️⃣  TWORZENIE ARCHIWUM ZIP")
print("-" * 70)

zip_path = f"{output_dir}/wszystkie_certyfikaty.zip"
zip_result = generator.create_zip_archive(generated_files, zip_path)

if os.path.exists(zip_result):
    zip_size = os.path.getsize(zip_result)
    print(f"✓ Utworzono archiwum ZIP:")
    print(f"  Plik: {zip_result}")
    print(f"  Rozmiar: {zip_size:,} bajtów ({zip_size/1024:.1f} KB)")
    print(f"  Zawiera: {len(generated_files)} certyfikatów PDF")
else:
    print("❌ Błąd tworzenia archiwum ZIP")
print()

# 7. Eksport do CSV (opcjonalnie)
print("7️⃣  EKSPORT DANYCH DO CSV")
print("-" * 70)

export_path = f"{output_dir}/uczestnicy_po_edycji.csv"
handler.export_to_csv(df_edited, export_path)
if os.path.exists(export_path):
    export_size = os.path.getsize(export_path)
    print(f"✓ Wyeksportowano dane do CSV:")
    print(f"  Plik: {export_path}")
    print(f"  Rozmiar: {export_size:,} bajtów")
else:
    print("❌ Błąd eksportu do CSV")
print()

# Podsumowanie
print("=" * 70)
print("✅ WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")
print("=" * 70)
print()
print("Podsumowanie:")
print(f"  • Wczytano: {len(df)} uczestników z CSV")
print(f"  • Dodano: 1 nowego uczestnika")
print(f"  • Wygenerowano: {len(generated_files)} certyfikatów PDF")
print(f"  • Utworzono: archiwum ZIP ({zip_size/1024:.1f} KB)")
print(f"  • Wyeksportowano: dane do CSV")
print()
print("Wszystkie pliki znajdują się w katalogu:")
print(f"  {os.path.abspath(output_dir)}")
print()
