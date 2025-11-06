# CertificateGenerator - Dokumentacja

## Przegląd

`CertificateGenerator` to klasa do generowania profesjonalnych certyfikatów PDF używając biblioteki ReportLab. Tworzy certyfikaty w formacie A4 landscape z eleganckim layoutem i obsługą polskich znaków.

## Instalacja

```bash
pip install reportlab
```

## Funkcje

- ✅ **Format A4 landscape** - profesjonalny układ poziomy
- ✅ **Ozdobna ramka** - podwójna ramka z ozdobnymi narożnikami
- ✅ **Logo organizacji** - opcjonalne logo na górze certyfikatu
- ✅ **Polskie znaki** - pełna obsługa znaków diakrytycznych
- ✅ **Elegancki layout** - profesjonalny układ treści
- ✅ **Generowanie wsadowe** - wiele certyfikatów jednocześnie
- ✅ **Archiwum ZIP** - pakowanie certyfikatów do ZIP
- ✅ **Progress bar** - monitorowanie postępu generowania

## Podstawowe użycie

### 1. Import i inicjalizacja

```python
from modules.pdf_generator import CertificateGenerator

# Bez logo
generator = CertificateGenerator()

# Z logo
generator = CertificateGenerator(logo_path='assets/logo.png')
```

### 2. Pojedynczy certyfikat

```python
# Dane uczestnika
participant = {
    'imie': 'Jan',
    'nazwisko': 'Kowalski',
    'warsztat': 'Python dla początkujących',
    'data': '15 stycznia 2025'
}

# Generuj certyfikat
success = generator.generate_certificate(
    participant,
    'output/certyfikat.pdf'
)

if success:
    print("Certyfikat wygenerowany!")
```

### 3. Generowanie wsadowe

```python
participants = [
    {'imie': 'Jan', 'nazwisko': 'Kowalski', 'warsztat': 'Python', 'data': '2025-01-15'},
    {'imie': 'Anna', 'nazwisko': 'Nowak', 'warsztat': 'Python', 'data': '2025-01-15'},
    {'imie': 'Piotr', 'nazwisko': 'Wiśniewski', 'warsztat': 'Python', 'data': '2025-01-15'}
]

files, success, errors = generator.generate_batch(
    participants,
    'output',
    show_progress=True
)

print(f"Wygenerowano {success} certyfikatów")
```

### 4. Tworzenie archiwum ZIP

```python
# Najpierw wygeneruj certyfikaty
files, success, errors = generator.generate_batch(participants, 'output')

# Utwórz archiwum ZIP
zip_path = generator.create_zip_archive(files, 'certyfikaty.zip')
print(f"Archiwum utworzone: {zip_path}")
```

## API Reference

### CertificateGenerator()

```python
generator = CertificateGenerator(
    template_path=None,  # Nie używane (dla kompatybilności)
    logo_path=None       # Ścieżka do logo PNG
)
```

**Parametry:**
- `template_path` (Optional[str]): Nie używane w ReportLab, zachowane dla kompatybilności API
- `logo_path` (Optional[str]): Ścieżka do pliku logo (PNG, JPG)

### generate_certificate()

```python
success = generator.generate_certificate(
    participant_data,  # Dict z danymi uczestnika
    output_path        # Ścieżka do pliku PDF
)
```

**Parametry:**
- `participant_data` (Dict[str, str]): Słownik z kluczami:
  - `imie`: Imię uczestnika
  - `nazwisko`: Nazwisko uczestnika
  - `warsztat`: Nazwa warsztatu
  - `data`: Data warsztatu
- `output_path` (str): Ścieżka do zapisu PDF

**Zwraca:**
- `bool`: True jeśli sukces, False w przypadku błędu

### generate_batch()

```python
files, success, errors = generator.generate_batch(
    participants_list,  # Lista uczestników
    output_dir,         # Katalog wyjściowy
    show_progress=True  # Pokazuj postęp
)
```

**Parametry:**
- `participants_list` (List[Dict[str, str]]): Lista słowników z danymi uczestników
- `output_dir` (str): Katalog wyjściowy dla certyfikatów
- `show_progress` (bool): Czy wyświetlać progress bar

**Zwraca:**
- `Tuple[List[str], int, int]`: (lista_plików, liczba_sukcesów, liczba_błędów)

**Nazwy plików:**
Automatycznie generowane jako: `Certyfikat_{Nazwisko}_{Imie}.pdf`

### create_zip_archive()

```python
zip_path = generator.create_zip_archive(
    pdf_files,              # Lista ścieżek do PDF
    zip_name='certyfikaty.zip'  # Nazwa archiwum
)
```

**Parametry:**
- `pdf_files` (List[str]): Lista ścieżek do plików PDF
- `zip_name` (str): Nazwa pliku ZIP

**Zwraca:**
- `Optional[str]`: Ścieżka do archiwum lub None w przypadku błędu

## Layout certyfikatu

```
┌─────────────────────────────────────────────────┐
│  ╔═══════════════════════════════════════════╗  │
│  ║                                           ║  │
│  ║             [LOGO] (opcjonalne)           ║  │
│  ║                                           ║  │
│  ║              CERTYFIKAT                   ║  │
│  ║         ─────────────────────             ║  │
│  ║                                           ║  │
│  ║    Niniejszym poświadcza się, że         ║  │
│  ║                                           ║  │
│  ║         Jan Kowalski                      ║  │
│  ║         ─────────────                     ║  │
│  ║                                           ║  │
│  ║        ukończył/a warsztat:              ║  │
│  ║                                           ║  │
│  ║    Python dla początkujących             ║  │
│  ║                                           ║  │
│  ║        w dniu 15 stycznia 2025           ║  │
│  ║                                           ║  │
│  ║                                           ║  │
│  ║   ─────────────      ─────────────       ║  │
│  ║    Organizator         Prowadzący        ║  │
│  ╚═══════════════════════════════════════════╝  │
└─────────────────────────────────────────────────┘
```

## Styl graficzny

### Kolory

- **Główny tekst**: `#2c3e50` (ciemny niebieski-szary)
- **Akcenty**: `#3498db` (niebieski)
- **Tekst pomocniczy**: `#555555` (szary)
- **Ramki**: `#2c3e50` i `#3498db`

### Czcionki

- **Tytuł**: Helvetica-Bold, 48pt
- **Imię i nazwisko**: Helvetica-Bold, 36pt
- **Nazwa warsztatu**: Helvetica-BoldOblique, 24pt
- **Tekst standardowy**: Helvetica, 16pt
- **Data**: Helvetica, 14pt
- **Podpisy**: Helvetica, 10pt

### Wymiary

- **Format**: A4 landscape (297mm x 210mm)
- **Marginesy**: 20mm
- **Ramka wewnętrzna**: +5mm od zewnętrznej

## Przykłady

### Integracja z DataHandler

```python
from modules.data_handler import DataHandler
from modules.pdf_generator import CertificateGenerator

# Wczytaj dane z CSV
handler = DataHandler()
df = handler.load_participants('data/participants.csv')

# Waliduj
errors = handler.validate_data(df)
if errors:
    print("Ostrzeżenia:", errors)

# Konwertuj do listy
participants = handler.get_participants_list(df)

# Generuj certyfikaty
generator = CertificateGenerator(logo_path='assets/logo.png')
files, success, errors = generator.generate_batch(
    participants,
    'output',
    show_progress=True
)

# Utwórz archiwum
zip_path = generator.create_zip_archive(files, 'certyfikaty.zip')
print(f"Gotowe! Archiwum: {zip_path}")
```

### Polskie znaki

```python
participant = {
    'imie': 'Łukasz',
    'nazwisko': 'Żółciński',
    'warsztat': 'Szkolenie z Pythona - część I',
    'data': '15 stycznia 2025 r.'
}

generator = CertificateGenerator()
generator.generate_certificate(participant, 'certyfikat.pdf')
```

### Długie nazwy warsztatów

Automatyczne dostosowanie rozmiaru czcionki dla długich nazw:

```python
participant = {
    'imie': 'Jan',
    'nazwisko': 'Kowalski',
    'warsztat': 'Zaawansowane programowanie w Pythonie z wykorzystaniem frameworków Django i Flask',
    'data': '2025-01-15'
}

# Automatycznie użyje mniejszej czcionki
generator.generate_certificate(participant, 'certyfikat.pdf')
```

### Progress bar w pętli

```python
participants = load_many_participants()  # 100+ uczestników

generator = CertificateGenerator()

# Pokazuje progress: "Generowanie [1/100]: Jan Kowalski..."
files, success, errors = generator.generate_batch(
    participants,
    'output',
    show_progress=True
)
```

## Testowanie

Uruchom testy:

```bash
cd certyfikator
python3 test_certificate_generator.py
```

Uruchom demo:

```bash
python3 demo_certificate_generator.py
```

## Porównanie z PDFGenerator

| Funkcja | CertificateGenerator | PDFGenerator |
|---------|---------------------|--------------|
| Biblioteka | ReportLab | WeasyPrint |
| Szablon | Programowy (Python) | HTML/CSS |
| Polskie znaki | ✅ Automatyczne | ✅ Automatyczne |
| Logo | ✅ Wbudowane | ⚠️ Wymaga HTML |
| Layout | ✅ Stały, elegancki | ✅ Dowolny (CSS) |
| Łatwość użycia | ✅✅✅ Prosty API | ⚠️ Wymaga HTML |
| Wydajność | ✅✅✅ Szybki | ⚠️ Wolniejszy |
| ZIP | ✅ Wbudowane | ❌ Brak |
| Progress | ✅ Wbudowany | ❌ Brak |

## Rozwiązywanie problemów

### Błąd: "ReportLab nie jest zainstalowany"

```bash
pip install reportlab
```

### Logo nie wyświetla się

1. Sprawdź czy plik istnieje
2. Obsługiwane formaty: PNG, JPG
3. Zalecany rozmiar: 400x400 pikseli

```python
import os
logo_path = 'assets/logo.png'
if os.path.exists(logo_path):
    print("Logo OK")
else:
    print("Logo nie znalezione")
```

### Polskie znaki wyświetlają się nieprawidłowo

ReportLab automatycznie obsługuje polskie znaki w czcionce Helvetica. Jeśli masz problemy:

1. Sprawdź kodowanie danych wejściowych (UTF-8)
2. Upewnij się, że używasz najnowszej wersji ReportLab

```bash
pip install --upgrade reportlab
```

### Długa nazwa warsztatu wychodzi poza margines

Generator automatycznie zmniejsza czcionkę dla długich nazw. Jeśli to nie wystarcza, skróć nazwę warsztatu w danych wejściowych.

## Najlepsze praktyki

### 1. Waliduj dane przed generowaniem

```python
handler = DataHandler()
df = handler.load_participants('data.csv')

errors = handler.validate_data(df)
if errors:
    print("Napraw błędy przed generowaniem")
    exit(1)
```

### 2. Zawsze twórz backup

```python
import shutil
import time

# Backup przed generowaniem
timestamp = time.strftime('%Y%m%d_%H%M%S')
backup_dir = f'backup/output_{timestamp}'
shutil.copytree('output', backup_dir)
```

### 3. Używaj archiwów ZIP dla wielu certyfikatów

```python
# Nie wysyłaj 100 plików PDF oddzielnie
# Utwórz jedno archiwum
files, _, _ = generator.generate_batch(participants, 'output')
zip_path = generator.create_zip_archive(files, 'certyfikaty.zip')

# Teraz masz jeden plik do wysłania
```

### 4. Testuj na małej próbce

```python
# Przed generowaniem 1000 certyfikatów
# Najpierw przetestuj na 3
test_sample = participants[:3]
generator.generate_batch(test_sample, 'test_output')

# Sprawdź wyniki, potem generuj wszystkie
```

## Licencja

MIT

## Wsparcie

W przypadku problemów sprawdź:
- [Dokumentację ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- `test_certificate_generator.py` - przykłady użycia
- `demo_certificate_generator.py` - demonstracja
