"""
Moduł do obsługi danych CSV i Excel
"""

import pandas as pd
import os


class DataHandler:
    """Klasa do obsługi danych uczestników z plików CSV i Excel"""

    def __init__(self):
        """Inicjalizacja handlera danych"""
        self.data = None
        self.file_path = None

    def load_csv(self, file_path, encoding='utf-8'):
        """
        Wczytuje dane z pliku CSV

        Args:
            file_path (str): Ścieżka do pliku CSV
            encoding (str): Kodowanie pliku (domyślnie utf-8)

        Returns:
            pd.DataFrame: DataFrame z danymi lub None w przypadku błędu
        """
        try:
            self.data = pd.read_csv(file_path, encoding=encoding)
            self.file_path = file_path
            return self.data

        except Exception as e:
            print(f"Błąd podczas wczytywania CSV: {e}")
            return None

    def load_excel(self, file_path, sheet_name=0):
        """
        Wczytuje dane z pliku Excel

        Args:
            file_path (str): Ścieżka do pliku Excel
            sheet_name (str/int): Nazwa lub indeks arkusza

        Returns:
            pd.DataFrame: DataFrame z danymi lub None w przypadku błędu
        """
        try:
            self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            self.file_path = file_path
            return self.data

        except Exception as e:
            print(f"Błąd podczas wczytywania Excel: {e}")
            return None

    def load_file(self, file_path):
        """
        Automatycznie wykrywa typ pliku i wczytuje dane

        Args:
            file_path (str): Ścieżka do pliku

        Returns:
            pd.DataFrame: DataFrame z danymi lub None w przypadku błędu
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.csv':
            return self.load_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self.load_excel(file_path)
        else:
            print(f"Nieobsługiwany format pliku: {ext}")
            return None

    def validate_columns(self, required_columns):
        """
        Sprawdza czy DataFrame zawiera wymagane kolumny

        Args:
            required_columns (list): Lista wymaganych nazw kolumn

        Returns:
            tuple: (bool, list) - (czy_poprawne, brakujące_kolumny)
        """
        if self.data is None:
            return False, required_columns

        missing_columns = [col for col in required_columns if col not in self.data.columns]

        return len(missing_columns) == 0, missing_columns

    def get_participants_list(self, column_mapping=None):
        """
        Zwraca listę słowników z danymi uczestników

        Args:
            column_mapping (dict, optional): Mapowanie nazw kolumn
                Przykład: {'Imię': 'imie', 'Nazwisko': 'nazwisko'}

        Returns:
            list: Lista słowników z danymi uczestników
        """
        if self.data is None:
            return []

        # Jeśli nie ma mapowania, użyj domyślnego
        if column_mapping is None:
            column_mapping = {
                'Imię': 'imie',
                'Nazwisko': 'nazwisko',
                'Email': 'email',
                'Warsztat': 'warsztat',
                'Data': 'data'
            }

        # Przekształć DataFrame na listę słowników
        participants = []
        for _, row in self.data.iterrows():
            participant = {}
            for old_name, new_name in column_mapping.items():
                if old_name in self.data.columns:
                    participant[new_name] = row[old_name]

            participants.append(participant)

        return participants

    def save_to_csv(self, output_path, encoding='utf-8'):
        """
        Zapisuje dane do pliku CSV

        Args:
            output_path (str): Ścieżka do pliku wyjściowego
            encoding (str): Kodowanie pliku

        Returns:
            bool: True jeśli sukces, False w przypadku błędu
        """
        if self.data is None:
            return False

        try:
            self.data.to_csv(output_path, index=False, encoding=encoding)
            return True

        except Exception as e:
            print(f"Błąd podczas zapisywania CSV: {e}")
            return False

    def save_to_excel(self, output_path):
        """
        Zapisuje dane do pliku Excel

        Args:
            output_path (str): Ścieżka do pliku wyjściowego

        Returns:
            bool: True jeśli sukces, False w przypadku błędu
        """
        if self.data is None:
            return False

        try:
            self.data.to_excel(output_path, index=False)
            return True

        except Exception as e:
            print(f"Błąd podczas zapisywania Excel: {e}")
            return False

    def filter_by_attendance(self, attendance_names):
        """
        Filtruje dane uczestników na podstawie listy obecności

        Args:
            attendance_names (list): Lista krotek (imię, nazwisko)

        Returns:
            pd.DataFrame: Przefiltrowane dane
        """
        if self.data is None:
            return None

        # Stwórz zestaw imion i nazwisk z listy obecności
        attendance_set = set(
            (str(imie).lower(), str(nazwisko).lower())
            for imie, nazwisko in attendance_names
        )

        # Filtruj DataFrame
        mask = self.data.apply(
            lambda row: (
                str(row.get('Imię', '')).lower(),
                str(row.get('Nazwisko', '')).lower()
            ) in attendance_set,
            axis=1
        )

        return self.data[mask]
