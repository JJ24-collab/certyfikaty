# 📜 Certyfikator

Aplikacja do automatycznego generowania certyfikatów dla uczestników warsztatów i szkoleń.

## ✨ Funkcje

- ✅ **Generowanie certyfikatów PDF** z szablonów HTML
- ✅ **Obsługa danych** z plików CSV i Excel
- ✅ **OCR dla list obecności** - automatyczne wyciąganie imion z skanów
- ✅ **Zarządzanie szablonami** - tworzenie i edycja własnych szablonów
- ✅ **Wsadowe generowanie** - wiele certyfikatów jednocześnie
- ✅ **Interfejs webowy** - przyjazny interfejs Streamlit

## 📋 Wymagania

### System

- Python 3.8 lub nowszy
- pip (menedżer pakietów Python)

### Opcjonalnie (dla OCR)

- Tesseract OCR
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr tesseract-ocr-pol`
  - macOS: `brew install tesseract tesseract-lang`
  - Windows: [Pobierz instalator](https://github.com/UB-Mannheim/tesseract/wiki)

### Zależności WeasyPrint

WeasyPrint wymaga dodatkowych bibliotek systemowych:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
```

**macOS:**
```bash
brew install python3 cairo pango gdk-pixbuf libffi
```

**Windows:**
Zainstaluj [GTK+ for Windows Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

## 🚀 Instalacja

### 1. Klonowanie repozytorium

```bash
git clone <repository-url>
cd certyfikator
```

### 2. Utworzenie środowiska wirtualnego (zalecane)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate  # Windows
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

## 🎯 Uruchomienie

### Uruchomienie aplikacji

```bash
streamlit run app.py
```

Aplikacja otworzy się automatycznie w przeglądarce pod adresem `http://localhost:8501`

### Pierwszy test

1. Otwórz aplikację w przeglądarce
2. Przejdź do zakładki "Generuj certyfikaty"
3. Wybierz szablon "szablon_podstawowy.html"
4. Wgraj plik `data/example_participants.csv`
5. Kliknij "Generuj wszystkie certyfikaty"
6. Certyfikaty zostaną zapisane w folderze `output/`

## 📁 Struktura projektu

```
certyfikator/
├── app.py                          # Główna aplikacja Streamlit
├── modules/                        # Moduły aplikacji
│   ├── __init__.py
│   ├── pdf_generator.py            # Generowanie PDF
│   ├── ocr_processor.py            # OCR dla list obecności
│   ├── data_handler.py             # Obsługa CSV/Excel
│   └── template_manager.py         # Zarządzanie szablonami
├── templates/                      # Szablony HTML certyfikatów
│   └── szablon_podstawowy.html
├── data/                           # Dane wejściowe
│   ├── example_participants.csv    # Przykładowe dane
│   └── attendance/                 # Skany list obecności
├── output/                         # Wygenerowane certyfikaty
├── assets/                         # Zasoby (logo itp.)
├── requirements.txt                # Zależności Python
└── README.md                       # Ten plik
```

## 📝 Format danych wejściowych

### CSV/Excel

Plik z danymi uczestników musi zawierać następujące kolumny:

| Kolumna   | Opis                    | Przykład                    |
|-----------|-------------------------|-----------------------------|
| Imię      | Imię uczestnika         | Jan                         |
| Nazwisko  | Nazwisko uczestnika     | Kowalski                    |
| Email     | Adres email             | jan.kowalski@example.com    |
| Warsztat  | Nazwa warsztatu         | Python dla początkujących   |
| Data      | Data warsztatu          | 2025-01-15                  |

### Przykład CSV:

```csv
Imię,Nazwisko,Email,Warsztat,Data
Jan,Kowalski,jan.kowalski@example.com,Python dla początkujących,2025-01-15
Anna,Nowak,anna.nowak@example.com,Python dla początkujących,2025-01-15
```

## 🎨 Tworzenie własnych szablonów

### W interfejsie aplikacji:

1. Przejdź do zakładki "Zarządzaj szablonami"
2. Kliknij "Utwórz nowy szablon"
3. Wprowadź nazwę i tytuł certyfikatu
4. Opcjonalnie dodaj własny CSS
5. Zapisz szablon

### Zmienne dostępne w szablonach:

- `{imie}` - Imię uczestnika
- `{nazwisko}` - Nazwisko uczestnika
- `{email}` - Email uczestnika
- `{warsztat}` - Nazwa warsztatu
- `{data}` - Data warsztatu

### Przykład użycia w HTML:

```html
<h2>{imie} {nazwisko}</h2>
<p>ukończył/a warsztat: {warsztat}</p>
<p>w dniu: {data}</p>
```

## 🔧 Konfiguracja OCR

### Instalacja Tesseract z polskim językiem:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-pol
```

**macOS:**
```bash
brew install tesseract
brew install tesseract-lang
```

**Windows:**
1. Pobierz instalator z [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Zainstaluj z obsługą języka polskiego
3. Dodaj ścieżkę do Tesseract do zmiennej PATH

### Użycie OCR:

1. Przejdź do zakładki "OCR listy obecności"
2. Wgraj skany list obecności (PNG, JPG, PDF)
3. Aplikacja automatycznie wyciągnie imiona i nazwiska
4. Eksportuj wyniki do CSV

## 🐛 Rozwiązywanie problemów

### Błąd: "ModuleNotFoundError: No module named 'PIL'"

```bash
pip install pillow
```

### Błąd: "OSError: cannot load library 'gobject-2.0-0'"

Zainstaluj biblioteki systemowe dla WeasyPrint (zobacz sekcję Wymagania)

### Błąd: "pytesseract.pytesseract.TesseractNotFoundError"

Zainstaluj Tesseract OCR (zobacz sekcję Konfiguracja OCR)

### Certyfikaty wyglądają źle w PDF

Upewnij się, że szablon HTML jest poprawnie sformatowany i używa stylów CSS kompatybilnych z WeasyPrint

## 📚 Wsparcie techniczne

- **Dokumentacja WeasyPrint:** https://doc.courtbouillon.org/weasyprint/
- **Dokumentacja Streamlit:** https://docs.streamlit.io/
- **Dokumentacja Tesseract:** https://github.com/tesseract-ocr/tesseract

## 📄 Licencja

Ten projekt jest dostępny na licencji MIT.

## 🤝 Wkład w rozwój

Zgłoszenia błędów i propozycje nowych funkcji są mile widziane!

1. Utwórz fork projektu
2. Stwórz branch dla nowej funkcji (`git checkout -b feature/amazing-feature`)
3. Commituj zmiany (`git commit -m 'Add some amazing feature'`)
4. Push do brancha (`git push origin feature/amazing-feature`)
5. Otwórz Pull Request

## ✨ Autorzy

Stworzony z ❤️ dla ułatwienia procesu generowania certyfikatów.

---

**Powodzenia w generowaniu certyfikatów! 📜**
