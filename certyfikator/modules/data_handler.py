"""
Moduł do obsługi danych CSV i Excel

Przykład użycia:
    >>> from modules.data_handler import DataHandler
    >>>
    >>> # Inicjalizacja handlera
    >>> handler = DataHandler()
    >>>
    >>> # Wczytanie danych
    >>> df = handler.load_participants('data/example_participants.csv')
    >>>
    >>> # Walidacja danych
    >>> errors = handler.validate_data(df)
    >>> if errors:
    >>>     print(f"Znaleziono błędy: {errors}")
    >>> else:
    >>>     print("Dane są poprawne")
    >>>
    >>> # Konwersja do listy słowników
    >>> participants = handler.get_participants_list(df)
    >>> for participant in participants:
    >>>     print(f"{participant['imie']} {participant['nazwisko']}")
    >>>
    >>> # Eksport do CSV
    >>> handler.export_to_csv(df, 'output/participants_clean.csv')
"""

import pandas as pd
import os
from typing import Optional, List, Dict, Tuple, Union


class DataHandler:
    """
    Klasa do obsługi danych uczestników z plików CSV i Excel

    Zapewnia funkcjonalność wczytywania, walidacji i eksportu danych uczestników
    warsztatów i szkoleń.

    Attributes:
        REQUIRED_COLUMNS (List[str]): Lista wymaganych kolumn w danych

    Example:
        >>> handler = DataHandler()
        >>> df = handler.load_participants('participants.csv')
        >>> if df is not None:
        >>>     errors = handler.validate_data(df)
        >>>     if not errors:
        >>>         participants = handler.get_participants_list(df)
    """

    REQUIRED_COLUMNS = ['Imię', 'Nazwisko', 'Warsztat', 'Data']

    def __init__(self):
        """Inicjalizuje handler danych"""
        pass

    def load_participants(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Wczytuje dane uczestników z pliku CSV lub Excel

        Automatycznie rozpoznaje format pliku na podstawie rozszerzenia
        i wczytuje dane. Obsługuje formaty .csv, .xlsx i .xls.
        Po wczytaniu przeprowadza podstawową walidację obecności wymaganych kolumn.

        Args:
            file_path (str): Ścieżka do pliku z danymi uczestników

        Returns:
            Optional[pd.DataFrame]: DataFrame z danymi uczestników lub None w przypadku błędu

        Raises:
            FileNotFoundError: Jeśli plik nie istnieje
            ValueError: Jeśli format pliku nie jest obsługiwany
            Exception: Dla innych błędów podczas wczytywania

        Example:
            >>> handler = DataHandler()
            >>> df = handler.load_participants('data/participants.csv')
            >>> if df is not None:
            >>>     print(f"Wczytano {len(df)} rekordów")
            >>>
            >>> # Obsługa Excela
            >>> df_excel = handler.load_participants('data/participants.xlsx')
        """
        # Sprawdź czy plik istnieje
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Plik nie istnieje: {file_path}")

        # Pobierz rozszerzenie pliku
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        try:
            # Wczytaj dane w zależności od formatu
            if ext == '.csv':
                # Próbuj różne kodowania
                for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1250']:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError(f"Nie udało się wczytać pliku CSV z żadnym wspieranym kodowaniem")

            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, sheet_name=0)

            else:
                raise ValueError(
                    f"Nieobsługiwany format pliku: {ext}. "
                    f"Obsługiwane formaty: .csv, .xlsx, .xls"
                )

            # Waliduj wymagane kolumny
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]

            if missing_columns:
                raise ValueError(
                    f"Brakujące wymagane kolumny: {', '.join(missing_columns)}. "
                    f"Wymagane kolumny: {', '.join(self.REQUIRED_COLUMNS)}"
                )

            return df

        except FileNotFoundError:
            raise
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Błąd podczas wczytywania pliku {file_path}: {str(e)}")

    def validate_data(self, df: pd.DataFrame) -> List[str]:
        """
        Sprawdza poprawność danych uczestników

        Przeprowadza następujące walidacje:
        - Sprawdza czy wszystkie wymagane pola są wypełnione
        - Wykrywa i raportuje duplikaty (te same Imię i Nazwisko)
        - Sprawdza poprawność formatu daty (jeśli możliwe)
        - Usuwa wiersze z pustymi wartościami w wymaganych kolumnach

        Args:
            df (pd.DataFrame): DataFrame z danymi uczestników do walidacji

        Returns:
            List[str]: Lista komunikatów o błędach. Pusta lista oznacza brak błędów.

        Example:
            >>> handler = DataHandler()
            >>> df = handler.load_participants('participants.csv')
            >>> errors = handler.validate_data(df)
            >>>
            >>> if errors:
            >>>     print("Znaleziono następujące problemy:")
            >>>     for error in errors:
            >>>         print(f"  - {error}")
            >>> else:
            >>>     print("Wszystkie dane są poprawne!")
        """
        errors = []

        if df is None or df.empty:
            errors.append("DataFrame jest pusty lub None")
            return errors

        # Sprawdź obecność wymaganych kolumn
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            errors.append(f"Brakujące kolumny: {', '.join(missing_columns)}")
            return errors

        # Sprawdź puste wartości w wymaganych kolumnach
        for col in self.REQUIRED_COLUMNS:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                errors.append(
                    f"Kolumna '{col}' zawiera {null_count} pustych wartości "
                    f"(wiersze: {df[df[col].isnull()].index.tolist()})"
                )

            # Sprawdź puste stringi
            if df[col].dtype == 'object':
                empty_strings = df[col].astype(str).str.strip().eq('').sum()
                if empty_strings > 0:
                    empty_indices = df[df[col].astype(str).str.strip().eq('')].index.tolist()
                    errors.append(
                        f"Kolumna '{col}' zawiera {empty_strings} pustych wartości tekstowych "
                        f"(wiersze: {empty_indices})"
                    )

        # Sprawdź duplikaty (to samo Imię i Nazwisko)
        if 'Imię' in df.columns and 'Nazwisko' in df.columns:
            # Utwórz kopię z normalizacją do porównania
            df_normalized = df.copy()
            df_normalized['Imię'] = df_normalized['Imię'].astype(str).str.strip().str.lower()
            df_normalized['Nazwisko'] = df_normalized['Nazwisko'].astype(str).str.strip().str.lower()

            duplicates = df_normalized[df_normalized.duplicated(subset=['Imię', 'Nazwisko'], keep=False)]

            if not duplicates.empty:
                duplicate_count = len(duplicates)
                duplicate_names = duplicates.groupby(['Imię', 'Nazwisko']).size()
                duplicate_list = [
                    f"{name[0].title()} {name[1].title()} ({count}x)"
                    for name, count in duplicate_names.items()
                ]
                errors.append(
                    f"Znaleziono {duplicate_count} duplikatów uczestników: "
                    f"{', '.join(duplicate_list)}"
                )

        # Sprawdź format daty (opcjonalnie)
        if 'Data' in df.columns:
            try:
                # Spróbuj przekonwertować na datę
                pd.to_datetime(df['Data'], errors='coerce')
                invalid_dates = df[pd.to_datetime(df['Data'], errors='coerce').isnull()]

                if not invalid_dates.empty and len(invalid_dates) < len(df):
                    # Są jakieś nieprawidłowe daty, ale nie wszystkie
                    errors.append(
                        f"Kolumna 'Data' zawiera {len(invalid_dates)} nieprawidłowych dat "
                        f"(wiersze: {invalid_dates.index.tolist()})"
                    )
            except Exception:
                # Jeśli konwersja się nie powiedzie, pomiń walidację dat
                pass

        # Sprawdź Email jeśli istnieje
        if 'Email' in df.columns:
            # Proste sprawdzenie formatu email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            invalid_emails = df[
                df['Email'].notna() &
                ~df['Email'].astype(str).str.match(email_pattern)
            ]

            if not invalid_emails.empty:
                errors.append(
                    f"Kolumna 'Email' zawiera {len(invalid_emails)} nieprawidłowych adresów email "
                    f"(wiersze: {invalid_emails.index.tolist()})"
                )

        return errors

    def export_to_csv(
        self,
        df: pd.DataFrame,
        output_path: str,
        encoding: str = 'utf-8',
        remove_duplicates: bool = False
    ) -> bool:
        """
        Zapisuje przetworzone dane do pliku CSV

        Eksportuje DataFrame do pliku CSV z możliwością usunięcia duplikatów
        przed zapisem.

        Args:
            df (pd.DataFrame): DataFrame z danymi do eksportu
            output_path (str): Ścieżka do pliku wyjściowego CSV
            encoding (str, optional): Kodowanie pliku. Domyślnie 'utf-8'.
            remove_duplicates (bool, optional): Czy usunąć duplikaty przed zapisem.
                Domyślnie False.

        Returns:
            bool: True jeśli zapis się powiódł, False w przypadku błędu

        Raises:
            Exception: W przypadku błędu podczas zapisu

        Example:
            >>> handler = DataHandler()
            >>> df = handler.load_participants('input.csv')
            >>>
            >>> # Prosty eksport
            >>> handler.export_to_csv(df, 'output/clean_data.csv')
            >>>
            >>> # Eksport z usunięciem duplikatów
            >>> handler.export_to_csv(
            >>>     df,
            >>>     'output/unique_participants.csv',
            >>>     remove_duplicates=True
            >>> )
        """
        if df is None or df.empty:
            raise ValueError("DataFrame jest pusty lub None")

        try:
            # Utwórz katalog jeśli nie istnieje
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # Usuń duplikaty jeśli wymagane
            df_to_save = df.copy()
            if remove_duplicates and 'Imię' in df.columns and 'Nazwisko' in df.columns:
                df_to_save = df_to_save.drop_duplicates(subset=['Imię', 'Nazwisko'], keep='first')

            # Zapisz do CSV
            df_to_save.to_csv(output_path, index=False, encoding=encoding)

            return True

        except Exception as e:
            raise Exception(f"Błąd podczas zapisywania CSV do {output_path}: {str(e)}")

    def get_participants_list(
        self,
        df: pd.DataFrame,
        column_mapping: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        """
        Zwraca listę słowników z danymi uczestników

        Konwertuje DataFrame na listę słowników, gdzie każdy słownik reprezentuje
        jednego uczestnika. Umożliwia mapowanie nazw kolumn na niestandardowe klucze.

        Args:
            df (pd.DataFrame): DataFrame z danymi uczestników
            column_mapping (Optional[Dict[str, str]], optional): Słownik mapowania kolumn.
                Klucz: nazwa kolumny w DataFrame, Wartość: klucz w wynikowym słowniku.
                Jeśli None, używa domyślnego mapowania.
                Domyślnie None.

        Returns:
            List[Dict[str, str]]: Lista słowników z danymi uczestników

        Example:
            >>> handler = DataHandler()
            >>> df = handler.load_participants('participants.csv')
            >>>
            >>> # Użycie domyślnego mapowania
            >>> participants = handler.get_participants_list(df)
            >>> for p in participants:
            >>>     print(f"{p['imie']} {p['nazwisko']} - {p['warsztat']}")
            >>>
            >>> # Własne mapowanie kolumn
            >>> custom_mapping = {
            >>>     'Imię': 'first_name',
            >>>     'Nazwisko': 'last_name',
            >>>     'Email': 'email',
            >>>     'Warsztat': 'workshop',
            >>>     'Data': 'date'
            >>> }
            >>> participants = handler.get_participants_list(df, custom_mapping)
            >>> print(participants[0]['first_name'])
        """
        if df is None or df.empty:
            return []

        # Domyślne mapowanie kolumn
        if column_mapping is None:
            column_mapping = {
                'Imię': 'imie',
                'Nazwisko': 'nazwisko',
                'Email': 'email',
                'Warsztat': 'warsztat',
                'Data': 'data'
            }

        # Konwertuj DataFrame na listę słowników
        participants = []

        for _, row in df.iterrows():
            participant = {}

            for source_col, target_key in column_mapping.items():
                if source_col in df.columns:
                    value = row[source_col]
                    # Konwertuj NaN na pusty string
                    if pd.isna(value):
                        participant[target_key] = ''
                    else:
                        participant[target_key] = str(value).strip()

            participants.append(participant)

        return participants

    # Metody pomocnicze (zachowane z poprzedniej wersji dla kompatybilności)

    def remove_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """
        Usuwa duplikaty z DataFrame

        Args:
            df (pd.DataFrame): DataFrame z danymi

        Returns:
            Tuple[pd.DataFrame, int]: (DataFrame bez duplikatów, liczba usuniętych duplikatów)

        Example:
            >>> handler = DataHandler()
            >>> df = handler.load_participants('participants.csv')
            >>> df_clean, removed_count = handler.remove_duplicates(df)
            >>> print(f"Usunięto {removed_count} duplikatów")
        """
        if df is None or df.empty:
            return df, 0

        original_count = len(df)

        if 'Imię' in df.columns and 'Nazwisko' in df.columns:
            df_clean = df.drop_duplicates(subset=['Imię', 'Nazwisko'], keep='first')
        else:
            df_clean = df.drop_duplicates()

        removed_count = original_count - len(df_clean)

        return df_clean, removed_count

    def filter_by_attendance(
        self,
        df: pd.DataFrame,
        attendance_names: List[Tuple[str, str]]
    ) -> pd.DataFrame:
        """
        Filtruje dane uczestników na podstawie listy obecności

        Args:
            df (pd.DataFrame): DataFrame z danymi uczestników
            attendance_names (List[Tuple[str, str]]): Lista krotek (imię, nazwisko)

        Returns:
            pd.DataFrame: Przefiltrowane dane

        Example:
            >>> handler = DataHandler()
            >>> df = handler.load_participants('all_participants.csv')
            >>> attendance = [('Jan', 'Kowalski'), ('Anna', 'Nowak')]
            >>> df_present = handler.filter_by_attendance(df, attendance)
            >>> print(f"Obecnych: {len(df_present)} osób")
        """
        if df is None or df.empty:
            return pd.DataFrame()

        # Stwórz zestaw imion i nazwisk z listy obecności (normalizacja)
        attendance_set = set(
            (str(imie).strip().lower(), str(nazwisko).strip().lower())
            for imie, nazwisko in attendance_names
        )

        # Filtruj DataFrame
        mask = df.apply(
            lambda row: (
                str(row.get('Imię', '')).strip().lower(),
                str(row.get('Nazwisko', '')).strip().lower()
            ) in attendance_set,
            axis=1
        )

        return df[mask]


# Przykład kompleksowego użycia
if __name__ == "__main__":
    """
    Przykład użycia klasy DataHandler

    Ten przykład pokazuje typowy workflow:
    1. Wczytanie danych
    2. Walidacja
    3. Czyszczenie (usunięcie duplikatów)
    4. Konwersja do listy
    5. Eksport
    """

    # Inicjalizacja
    handler = DataHandler()

    try:
        # 1. Wczytaj dane
        print("Wczytywanie danych...")
        df = handler.load_participants('data/example_participants.csv')
        print(f"✓ Wczytano {len(df)} rekordów")

        # 2. Waliduj dane
        print("\nWalidacja danych...")
        errors = handler.validate_data(df)

        if errors:
            print("✗ Znaleziono błędy:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✓ Dane są poprawne")

        # 3. Usuń duplikaty
        print("\nUsuwanie duplikatów...")
        df_clean, removed = handler.remove_duplicates(df)
        print(f"✓ Usunięto {removed} duplikatów")

        # 4. Konwertuj do listy słowników
        print("\nKonwersja do listy...")
        participants = handler.get_participants_list(df_clean)
        print(f"✓ Przygotowano {len(participants)} uczestników:")
        for p in participants[:3]:  # Pokaż pierwsze 3
            print(f"  - {p['imie']} {p['nazwisko']} ({p['warsztat']})")

        # 5. Eksportuj czyste dane
        print("\nEksport do CSV...")
        handler.export_to_csv(df_clean, 'output/participants_validated.csv')
        print("✓ Dane wyeksportowane do output/participants_validated.csv")

    except FileNotFoundError as e:
        print(f"✗ Błąd: {e}")
    except ValueError as e:
        print(f"✗ Błąd walidacji: {e}")
    except Exception as e:
        print(f"✗ Nieoczekiwany błąd: {e}")
