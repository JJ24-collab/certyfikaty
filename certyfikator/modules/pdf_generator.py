"""
Moduł do generowania certyfikatów PDF
"""

import os
from weasyprint import HTML
from datetime import datetime


class PDFGenerator:
    """Klasa do generowania certyfikatów PDF z szablonów HTML"""

    def __init__(self, template_path):
        """
        Inicjalizacja generatora PDF

        Args:
            template_path (str): Ścieżka do szablonu HTML
        """
        self.template_path = template_path

    def generate_certificate(self, participant_data, output_path):
        """
        Generuje certyfikat PDF dla uczestnika

        Args:
            participant_data (dict): Słownik z danymi uczestnika
                - imie: Imię uczestnika
                - nazwisko: Nazwisko uczestnika
                - warsztat: Nazwa warsztatu
                - data: Data warsztatu
                - email: Email uczestnika
            output_path (str): Ścieżka do zapisu pliku PDF

        Returns:
            bool: True jeśli sukces, False w przypadku błędu
        """
        try:
            # Wczytaj szablon HTML
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_html = f.read()

            # Zastąp placeholdery danymi uczestnika
            html_content = template_html.format(
                imie=participant_data.get('imie', ''),
                nazwisko=participant_data.get('nazwisko', ''),
                warsztat=participant_data.get('warsztat', ''),
                data=participant_data.get('data', ''),
                email=participant_data.get('email', '')
            )

            # Generuj PDF
            HTML(string=html_content).write_pdf(output_path)

            return True

        except Exception as e:
            print(f"Błąd podczas generowania certyfikatu: {e}")
            return False

    def generate_batch(self, participants_list, output_dir):
        """
        Generuje certyfikaty dla wielu uczestników

        Args:
            participants_list (list): Lista słowników z danymi uczestników
            output_dir (str): Katalog wyjściowy dla certyfikatów

        Returns:
            tuple: (liczba_sukcesów, liczba_błędów)
        """
        success_count = 0
        error_count = 0

        # Upewnij się, że katalog wyjściowy istnieje
        os.makedirs(output_dir, exist_ok=True)

        for participant in participants_list:
            # Generuj nazwę pliku
            filename = f"{participant.get('nazwisko', 'Unknown')}_{participant.get('imie', 'Unknown')}.pdf"
            filename = filename.replace(' ', '_')
            output_path = os.path.join(output_dir, filename)

            # Generuj certyfikat
            if self.generate_certificate(participant, output_path):
                success_count += 1
            else:
                error_count += 1

        return success_count, error_count
