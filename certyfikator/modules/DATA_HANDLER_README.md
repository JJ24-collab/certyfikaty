# DataHandler - Dokumentacja

## Przegląd

`DataHandler` to klasa do obsługi danych uczestników warsztatów i szkoleń. Zapewnia funkcjonalność wczytywania, walidacji i eksportu danych z plików CSV i Excel.

## Instalacja wymaganych bibliotek

```bash
pip install pandas openpyxl
```

## Podstawowe użycie

### 1. Inicjalizacja

```python
from modules.data_handler import DataHandler

handler = DataHandler()
```

### 2. Wczytywanie danych

```python
# Wczytaj dane z CSV lub Excel
df = handler.load_participants('data/participants.csv')
print(f"Wczytano {len(df)} rekordów")
```

**Obsługiwane formaty:**
- `.csv` - pliki CSV (z automatyczną detekcją kodowania)
- `.xlsx` - pliki Excel
- `.xls` - starsze pliki Excel

**Wymagane kolumny:**
- `Imię`
- `Nazwisko`
- `Warsztat`
- `Data`

Opcjonalne kolumny:
- `Email`

### 3. Walidacja danych

```python
# Sprawdź poprawność danych
errors = handler.validate_data(df)

if errors:
    print("Znaleziono błędy:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Dane są poprawne!")
```

**Sprawdzane aspekty:**
- ✓ Obecność wymaganych kolumn
- ✓ Puste wartości w wymaganych polach
- ✓ Duplikaty uczestników (Imię + Nazwisko)
- ✓ Format daty
- ✓ Format adresu email (jeśli kolumna istnieje)

### 4. Konwersja do listy słowników

```python
# Domyślne mapowanie
participants = handler.get_participants_list(df)

for participant in participants:
    print(f"{participant['imie']} {participant['nazwisko']}")
```

**Domyślne mapowanie:**
```python
{
    'Imię': 'imie',
    'Nazwisko': 'nazwisko',
    'Email': 'email',
    'Warsztat': 'warsztat',
    'Data': 'data'
}
```

**Własne mapowanie:**
```python
custom_mapping = {
    'Imię': 'first_name',
    'Nazwisko': 'last_name',
    'Email': 'email',
    'Warsztat': 'workshop',
    'Data': 'date'
}

participants = handler.get_participants_list(df, custom_mapping)
```

### 5. Eksport do CSV

```python
# Prosty eksport
handler.export_to_csv(df, 'output/participants.csv')

# Eksport z usunięciem duplikatów
handler.export_to_csv(
    df,
    'output/unique_participants.csv',
    remove_duplicates=True
)
```

## Metody dodatkowe

### remove_duplicates()

```python
df_clean, removed_count = handler.remove_duplicates(df)
print(f"Usunięto {removed_count} duplikatów")
```

### filter_by_attendance()

```python
# Lista obecności z OCR lub ręcznie wprowadzona
attendance = [
    ('Jan', 'Kowalski'),
    ('Anna', 'Nowak')
]

df_present = handler.filter_by_attendance(df, attendance)
print(f"Obecnych: {len(df_present)} osób")
```

## Kompletny przykład workflow

```python
from modules.data_handler import DataHandler

def process_participants(input_file):
    """Pełny workflow przetwarzania danych uczestników"""

    handler = DataHandler()

    try:
        # 1. Wczytaj dane
        print("Wczytywanie danych...")
        df = handler.load_participants(input_file)
        print(f"✓ Wczytano {len(df)} rekordów")

        # 2. Waliduj
        print("\nWalidacja...")
        errors = handler.validate_data(df)

        if errors:
            print("⚠ Ostrzeżenia:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✓ Dane poprawne")

        # 3. Usuń duplikaty
        print("\nUsuwanie duplikatów...")
        df_clean, removed = handler.remove_duplicates(df)
        print(f"✓ Usunięto {removed} duplikatów")

        # 4. Konwertuj
        print("\nPrzygotowanie listy uczestników...")
        participants = handler.get_participants_list(df_clean)
        print(f"✓ {len(participants)} uczestników gotowych")

        # 5. Eksportuj
        print("\nEksport...")
        handler.export_to_csv(df_clean, 'output/clean_participants.csv')
        print("✓ Zapisano w output/clean_participants.csv")

        return participants

    except FileNotFoundError as e:
        print(f"✗ Plik nie znaleziony: {e}")
    except ValueError as e:
        print(f"✗ Błąd walidacji: {e}")
    except Exception as e:
        print(f"✗ Nieoczekiwany błąd: {e}")

    return None

# Użycie
participants = process_participants('data/participants.csv')

if participants:
    # Generuj certyfikaty
    for p in participants:
        print(f"Generuję certyfikat dla {p['imie']} {p['nazwisko']}")
```

## Obsługa błędów

### FileNotFoundError
```python
try:
    df = handler.load_participants('nieistniejacy_plik.csv')
except FileNotFoundError as e:
    print(f"Plik nie istnieje: {e}")
```

### ValueError
```python
try:
    df = handler.load_participants('plik_bez_wymaganych_kolumn.csv')
except ValueError as e:
    print(f"Nieprawidłowy format danych: {e}")
```

### Ogólne błędy
```python
try:
    df = handler.load_participants('plik.csv')
    errors = handler.validate_data(df)
    participants = handler.get_participants_list(df)
except Exception as e:
    print(f"Wystąpił błąd: {e}")
```

## Testowanie

Uruchom testy przykładowe:

```bash
cd certyfikator
python3 test_data_handler.py
```

## Type hints

Wszystkie metody zawierają type hints dla lepszego wsparcia IDE:

```python
def load_participants(self, file_path: str) -> Optional[pd.DataFrame]: ...
def validate_data(self, df: pd.DataFrame) -> List[str]: ...
def export_to_csv(self, df: pd.DataFrame, output_path: str, ...) -> bool: ...
def get_participants_list(self, df: pd.DataFrame, ...) -> List[Dict[str, str]]: ...
```

## Format danych wejściowych

### CSV

```csv
Imię,Nazwisko,Email,Warsztat,Data
Jan,Kowalski,jan@example.com,Python,2025-01-15
Anna,Nowak,anna@example.com,Python,2025-01-15
```

### Excel

| Imię | Nazwisko | Email | Warsztat | Data |
|------|----------|-------|----------|------|
| Jan | Kowalski | jan@example.com | Python | 2025-01-15 |
| Anna | Nowak | anna@example.com | Python | 2025-01-15 |

## Rozwiązywanie problemów

### Błąd kodowania CSV

Klasa automatycznie próbuje różne kodowania:
- utf-8
- utf-8-sig
- latin-1
- cp1250

### Nieprawidłowe daty

Walidacja wykrywa nieprawidłowe formaty dat, ale nie blokuje przetwarzania.

### Duplikaty

Duplikaty są wykrywane na podstawie pary (Imię, Nazwisko) z normalizacją:
- Usuwanie białych znaków
- Konwersja do małych liter

## Najlepsze praktyki

1. **Zawsze waliduj dane po wczytaniu:**
   ```python
   df = handler.load_participants(file_path)
   errors = handler.validate_data(df)
   ```

2. **Obsługuj wyjątki:**
   ```python
   try:
       df = handler.load_participants(file_path)
   except (FileNotFoundError, ValueError) as e:
       # Obsłuż błąd
   ```

3. **Usuń duplikaty przed generowaniem certyfikatów:**
   ```python
   df_clean, removed = handler.remove_duplicates(df)
   ```

4. **Eksportuj przetworzone dane:**
   ```python
   handler.export_to_csv(df_clean, 'output/processed.csv')
   ```

## API Reference

### DataHandler

**Atrybuty:**
- `REQUIRED_COLUMNS` - Lista wymaganych kolumn

**Metody:**

| Metoda | Parametry | Zwraca | Opis |
|--------|-----------|--------|------|
| `load_participants()` | `file_path: str` | `Optional[pd.DataFrame]` | Wczytuje dane z CSV/Excel |
| `validate_data()` | `df: pd.DataFrame` | `List[str]` | Waliduje dane |
| `export_to_csv()` | `df, output_path, encoding, remove_duplicates` | `bool` | Eksportuje do CSV |
| `get_participants_list()` | `df, column_mapping` | `List[Dict[str, str]]` | Konwertuje do listy |
| `remove_duplicates()` | `df: pd.DataFrame` | `Tuple[pd.DataFrame, int]` | Usuwa duplikaty |
| `filter_by_attendance()` | `df, attendance_names` | `pd.DataFrame` | Filtruje według obecności |

## Licencja

MIT
