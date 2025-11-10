# 🚀 Quick Start - Certyfikator

## Szybkie uruchomienie aplikacji Streamlit

### 1️⃣ Instalacja zależności

```bash
cd certyfikator
pip install -r requirements.txt
```

### 2️⃣ Uruchomienie aplikacji

```bash
streamlit run app.py
```

Aplikacja otworzy się automatycznie w przeglądarce pod adresem: `http://localhost:8501`

### 3️⃣ Pierwsze kroki

#### Wersja ekspresowa (1 minuta):

1. **Pobierz przykładowy plik**
   - W aplikacji kliknij "⬇️ Pobierz przykład"
   - Zapisz plik `example_participants.csv`

2. **Wgraj plik**
   - Kliknij "Browse files"
   - Wybierz pobrany `example_participants.csv`

3. **Generuj certyfikaty**
   - Przewiń w dół do sekcji "Generowanie masowe"
   - Kliknij "🚀 Generuj wszystkie certyfikaty"
   - Poczekaj na zakończenie

4. **Pobierz wyniki**
   - Kliknij "📦 Pobierz wszystkie certyfikaty (ZIP)"
   - Rozpakuj archiwum
   - Gotowe! 🎉

#### Wersja z podglądem (2 minuty):

1. **Wgraj dane** (jak wyżej)

2. **Zobacz podgląd**
   - W sekcji "Podgląd certyfikatu"
   - Wybierz uczestnika z listy
   - Kliknij "👁️ Wygeneruj podgląd"
   - Kliknij "⬇️ Pobierz podgląd"
   - Otwórz PDF i sprawdź

3. **Generuj wszystkie** (jak wyżej)

#### Wersja z logo (3 minuty):

1. **Dodaj logo**
   - W sekcji "Konfiguracja certyfikatu"
   - Kliknij "Browse files" przy "Logo organizacji"
   - Wybierz plik PNG lub JPG (400x400 pikseli)

2. **Zmień konfigurację**
   - Wpisz nazwę organizacji
   - Wpisz osobę podpisującą
   - Wpisz stanowisko

3. **Generuj z logo**
   - Przewiń do "Generowanie masowe"
   - Kliknij "🚀 Generuj wszystkie certyfikaty"

## 📁 Struktura katalogów

Po uruchomieniu i wygenerowaniu certyfikatów:

```
certyfikator/
├── app.py                      # Aplikacja Streamlit
├── data/                       # Dane wejściowe
│   └── example_participants.csv
├── output/                     # Wygenerowane certyfikaty ✨
│   ├── Certyfikat_Kowalski_Jan.pdf
│   ├── Certyfikat_Nowak_Anna.pdf
│   └── certyfikaty.zip         # Archiwum ze wszystkimi
├── assets/                     # Logo organizacji
│   └── logo.png                # (opcjonalnie)
└── modules/                    # Moduły aplikacji
```

## 🎯 Funkcje aplikacji

### TAB 1: Generuj Certyfikaty

**Sekcje:**
1. 📤 **Upload pliku** - CSV lub Excel
2. 📊 **Edycja danych** - tabela z możliwością edycji
3. ✅ **Walidacja** - automatyczne sprawdzanie błędów
4. ⚙️ **Konfiguracja** - nazwa org, osoba podpisująca, logo
5. 👁️ **Podgląd** - generuj pojedynczy certyfikat
6. 🚀 **Generowanie masowe** - wszystkie certyfikaty + ZIP

**Statystyki:**
- Liczba uczestników
- Liczba kolumn
- Liczba warsztatów

**Progress bar:**
- Pokazuje postęp generowania
- Informuje o błędach

### TAB 2: Instrukcja

**Zawartość:**
- Format danych (tabela wymaganych kolumn)
- Proces krok po kroku
- FAQ (7 pytań)
- Wsparcie (kontakt)
- Download przykładowego pliku

### SIDEBAR

**Informacje:**
- O aplikacji
- Statystyki sesji (ile wygenerowano certyfikatów)
- Wersja i autor
- Lista funkcji
- Przycisk resetuj statystyki

## 📝 Format pliku CSV

### Minimalne wymagania:

```csv
Imię,Nazwisko,Warsztat,Data
Jan,Kowalski,Python,2025-01-15
Anna,Nowak,Python,2025-01-15
```

### Pełny format:

```csv
Imię,Nazwisko,Warsztat,Data,Email
Jan,Kowalski,Python dla początkujących,2025-01-15,jan@example.com
Anna,Nowak,Python dla początkujących,2025-01-15,anna@example.com
```

### Wymagane kolumny:
- ✅ **Imię** - wymagane
- ✅ **Nazwisko** - wymagane
- ✅ **Warsztat** - wymagane
- ✅ **Data** - wymagane
- ❌ **Email** - opcjonalne

## 🎨 Certyfikat

**Format:**
- A4 landscape (297mm x 210mm)
- Ozdobna ramka z narożnikami
- Logo organizacji (jeśli wgrane)

**Layout:**
- Tytuł "CERTYFIKAT"
- Imię i nazwisko (podkreślone)
- Nazwa warsztatu (niebieska, italic)
- Data
- Miejsca na podpisy

**Kolory:**
- Główny: `#2c3e50` (ciemny niebieski-szary)
- Akcent: `#3498db` (niebieski)

**Czcionki:**
- Helvetica (automatyczna obsługa polskich znaków)

## 🔧 Rozwiązywanie problemów

### Aplikacja się nie uruchamia

```bash
# Sprawdź czy zainstalowałeś zależności
pip install -r requirements.txt

# Sprawdź wersję Python (wymaga 3.8+)
python --version
```

### Błąd: "ModuleNotFoundError"

```bash
# Zainstaluj brakujący moduł
pip install <nazwa-modułu>

# Lub zainstaluj wszystkie zależności ponownie
pip install -r requirements.txt --force-reinstall
```

### Certyfikaty nie generują się

1. Sprawdź czy plik CSV ma wszystkie wymagane kolumny
2. Sprawdź kodowanie pliku (powinno być UTF-8)
3. Sprawdź czy w kolumnach nie ma pustych wartości
4. Zobacz szczegóły błędu w expanderze "Szczegóły błędu"

### Logo się nie wyświetla

1. Sprawdź format pliku (PNG, JPG)
2. Sprawdź rozmiar pliku (max 5 MB)
3. Zalecany rozmiar: 400x400 pikseli
4. Upewnij się, że kliknąłeś "Browse files" i wybrałeś plik

## 📞 Potrzebujesz pomocy?

- 📚 Pełna dokumentacja: `README.md`
- 📖 Instrukcja w aplikacji: TAB "Instrukcja"
- 🔍 FAQ w aplikacji: 7 odpowiedzi na najczęstsze pytania

## 🎓 Przykładowe scenariusze

### Scenariusz 1: Szybkie 5 certyfikatów

```bash
# 1. Uruchom aplikację
streamlit run app.py

# 2. W aplikacji:
# - Pobierz przykład
# - Wgraj pobrany plik
# - Generuj wszystkie

# 3. Pobierz ZIP
# Gotowe w <1 minuta!
```

### Scenariusz 2: Warsztat z logo

```bash
# 1. Przygotuj:
# - Plik CSV z uczestnikami
# - Logo PNG (400x400)

# 2. W aplikacji:
# - Wgraj CSV
# - Sprawdź dane w tabeli
# - Wgraj logo
# - Zmień nazwę organizacji
# - Generuj podgląd
# - Generuj wszystkie

# 3. Pobierz ZIP
```

### Scenariusz 3: Edycja danych

```bash
# 1. Wgraj CSV

# 2. W tabeli:
# - Edytuj nazwiska
# - Dodaj nowych uczestników (kliknij +)
# - Usuń duplikaty (zaznacz wiersz, kliknij -)

# 3. Generuj certyfikaty
```

## ✨ Wskazówki

💡 **Tip 1:** Zawsze sprawdzaj podgląd przed generowaniem wszystkich certyfikatów

💡 **Tip 2:** Używaj przycisku "Resetuj statystyki" przed nową sesją

💡 **Tip 3:** Trzymaj logo w assets/logo.png - będzie ładowane automatycznie

💡 **Tip 4:** Zapisuj swoje pliki CSV jako backup

💡 **Tip 5:** Certyfikaty w output/ nie są usuwane automatycznie - możesz je zachować

## 🚀 Następne kroki

Po opanowaniu podstaw:

1. Przeczytaj pełną dokumentację w `README.md`
2. Sprawdź dokumentację modułów:
   - `modules/CERTIFICATE_GENERATOR_README.md`
   - `modules/DATA_HANDLER_README.md`
3. Uruchom testy:
   ```bash
   python test_certificate_generator.py
   python test_data_handler.py
   ```
4. Zobacz demo:
   ```bash
   python demo_certificate_generator.py
   ```

---

**Gotowe!** Miłego generowania certyfikatów! 🎉
