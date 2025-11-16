"""
Moduł do generowania certyfikatów PDF
"""

import os
import zipfile
from datetime import datetime
from typing import List, Dict, Optional, Tuple, TYPE_CHECKING
from pathlib import Path

# WeasyPrint (dla PDFGenerator)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

# ReportLab (dla CertificateGenerator)
try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm, inch
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, Frame
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    # Dla type checking bez instalacji ReportLab
    if TYPE_CHECKING:
        from reportlab.pdfgen import canvas


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


class CertificateGenerator:
    """
    Klasa do generowania certyfikatów PDF używając ReportLab

    Generuje profesjonalne certyfikaty w formacie A4 landscape z:
    - Ozdobną ramką
    - Logo organizacji (opcjonalnie)
    - Eleganckim layoutem
    - Obsługą polskich znaków

    Example:
        >>> generator = CertificateGenerator(logo_path='assets/logo.png')
        >>> participant = {
        >>>     'imie': 'Jan',
        >>>     'nazwisko': 'Kowalski',
        >>>     'warsztat': 'Python dla początkujących',
        >>>     'data': '2025-01-15'
        >>> }
        >>> generator.generate_certificate(participant, 'output/certyfikat.pdf')
    """

    def __init__(self, template_path: Optional[str] = None, logo_path: Optional[str] = None):
        """
        Inicjalizacja generatora certyfikatów

        Args:
            template_path (Optional[str]): Ścieżka do szablonu (nie używana w ReportLab,
                ale zachowana dla kompatybilności API)
            logo_path (Optional[str]): Ścieżka do logo organizacji
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "ReportLab nie jest zainstalowany. "
                "Zainstaluj: pip install reportlab"
            )

        self.template_path = template_path
        self.logo_path = logo_path
        self.logo_exists = False

        # Sprawdź czy logo istnieje
        if logo_path and os.path.exists(logo_path):
            self.logo_exists = True

        # Wymiary strony A4 landscape
        self.page_width, self.page_height = landscape(A4)

        # Marginesy
        self.margin = 20 * mm

    def _setup_fonts(self, c: "canvas.Canvas") -> None:
        """
        Konfiguruje czcionki dla certyfikatu

        Args:
            c (canvas.Canvas): Obiekt canvas ReportLab
        """
        # Używamy wbudowanych czcionek Helvetica
        # ReportLab automatycznie obsługuje polskie znaki w Helvetica
        pass

    def _draw_decorative_border(self, c: "canvas.Canvas") -> None:
        """
        Rysuje ozdobną ramkę wokół certyfikatu

        Args:
            c (canvas.Canvas): Obiekt canvas ReportLab
        """
        # Zewnętrzna ramka
        c.setStrokeColor(colors.HexColor('#2c3e50'))
        c.setLineWidth(3)
        c.rect(
            self.margin,
            self.margin,
            self.page_width - 2 * self.margin,
            self.page_height - 2 * self.margin
        )

        # Wewnętrzna ramka
        inner_margin = self.margin + 5 * mm
        c.setStrokeColor(colors.HexColor('#3498db'))
        c.setLineWidth(1)
        c.rect(
            inner_margin,
            inner_margin,
            self.page_width - 2 * inner_margin,
            self.page_height - 2 * inner_margin
        )

        # Ozdobne narożniki
        corner_size = 20 * mm
        corner_offset = self.margin - 3

        # Lewy górny róg
        c.setStrokeColor(colors.HexColor('#3498db'))
        c.setLineWidth(2)
        c.line(corner_offset, self.page_height - corner_offset,
               corner_offset, self.page_height - corner_offset - corner_size)
        c.line(corner_offset, self.page_height - corner_offset,
               corner_offset + corner_size, self.page_height - corner_offset)

        # Prawy górny róg
        c.line(self.page_width - corner_offset, self.page_height - corner_offset,
               self.page_width - corner_offset, self.page_height - corner_offset - corner_size)
        c.line(self.page_width - corner_offset, self.page_height - corner_offset,
               self.page_width - corner_offset - corner_size, self.page_height - corner_offset)

        # Lewy dolny róg
        c.line(corner_offset, corner_offset,
               corner_offset, corner_offset + corner_size)
        c.line(corner_offset, corner_offset,
               corner_offset + corner_size, corner_offset)

        # Prawy dolny róg
        c.line(self.page_width - corner_offset, corner_offset,
               self.page_width - corner_offset, corner_offset + corner_size)
        c.line(self.page_width - corner_offset, corner_offset,
               self.page_width - corner_offset - corner_size, corner_offset)

    def _draw_logo(self, c: "canvas.Canvas") -> float:
        """
        Rysuje logo organizacji na górze certyfikatu

        Args:
            c (canvas.Canvas): Obiekt canvas ReportLab

        Returns:
            float: Wysokość logo (dla pozycjonowania kolejnych elementów)
        """
        if not self.logo_exists:
            return 0

        try:
            logo_height = 30 * mm
            logo_width = 30 * mm

            x = (self.page_width - logo_width) / 2
            y = self.page_height - self.margin - 40 * mm

            c.drawImage(
                self.logo_path,
                x, y,
                width=logo_width,
                height=logo_height,
                preserveAspectRatio=True,
                mask='auto'
            )

            return logo_height + 10 * mm

        except Exception as e:
            print(f"Nie można wczytać logo: {e}")
            return 0

    def _draw_title(self, c: "canvas.Canvas", y_position: float) -> float:
        """
        Rysuje tytuł "CERTYFIKAT"

        Args:
            c (canvas.Canvas): Obiekt canvas ReportLab
            y_position (float): Pozycja Y dla tytułu

        Returns:
            float: Nowa pozycja Y po narysowaniu tytułu
        """
        c.setFont("Helvetica-Bold", 48)
        c.setFillColor(colors.HexColor('#2c3e50'))

        title = "CERTYFIKAT"
        title_width = c.stringWidth(title, "Helvetica-Bold", 48)
        x = (self.page_width - title_width) / 2

        c.drawString(x, y_position, title)

        # Linia pod tytułem
        line_y = y_position - 8 * mm
        line_margin = 80 * mm
        c.setStrokeColor(colors.HexColor('#3498db'))
        c.setLineWidth(2)
        c.line(line_margin, line_y, self.page_width - line_margin, line_y)

        return y_position - 25 * mm

    def _draw_participant_info(
        self,
        c: "canvas.Canvas",
        participant_data: Dict[str, str],
        y_position: float
    ) -> float:
        """
        Rysuje informacje o uczestniku

        Args:
            c (canvas.Canvas): Obiekt canvas ReportLab
            participant_data (Dict[str, str]): Dane uczestnika
            y_position (float): Pozycja Y

        Returns:
            float: Nowa pozycja Y
        """
        # "Niniejszym poświadcza się, że"
        c.setFont("Helvetica", 16)
        c.setFillColor(colors.HexColor('#555555'))
        text = "Niniejszym poświadcza się, że"
        text_width = c.stringWidth(text, "Helvetica", 16)
        x = (self.page_width - text_width) / 2
        c.drawString(x, y_position, text)
        y_position -= 15 * mm

        # Imię i Nazwisko (duża, bold)
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(colors.HexColor('#2c3e50'))
        full_name = f"{participant_data.get('imie', '')} {participant_data.get('nazwisko', '')}"
        name_width = c.stringWidth(full_name, "Helvetica-Bold", 36)
        x = (self.page_width - name_width) / 2
        c.drawString(x, y_position, full_name)

        # Podkreślenie imienia i nazwiska
        underline_y = y_position - 3 * mm
        underline_padding = 10 * mm
        c.setStrokeColor(colors.HexColor('#3498db'))
        c.setLineWidth(1.5)
        c.line(
            x - underline_padding,
            underline_y,
            x + name_width + underline_padding,
            underline_y
        )

        y_position -= 20 * mm

        # "ukończył/a warsztat:"
        c.setFont("Helvetica", 16)
        c.setFillColor(colors.HexColor('#555555'))
        text = "ukończył/a warsztat:"
        text_width = c.stringWidth(text, "Helvetica", 16)
        x = (self.page_width - text_width) / 2
        c.drawString(x, y_position, text)
        y_position -= 12 * mm

        # Nazwa warsztatu
        c.setFont("Helvetica-BoldOblique", 24)
        c.setFillColor(colors.HexColor('#3498db'))
        workshop = participant_data.get('warsztat', '')

        # Obsługa długich nazw warsztatów (łamanie linii)
        max_width = self.page_width - 2 * self.margin - 80 * mm
        if c.stringWidth(workshop, "Helvetica-BoldOblique", 24) > max_width:
            # Jeśli nazwa jest za długa, użyj mniejszej czcionki
            c.setFont("Helvetica-BoldOblique", 20)

        workshop_width = c.stringWidth(workshop, "Helvetica-BoldOblique", 24)
        x = (self.page_width - workshop_width) / 2
        c.drawString(x, y_position, workshop)
        y_position -= 15 * mm

        # Data
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.HexColor('#555555'))
        date_text = f"w dniu {participant_data.get('data', '')}"
        date_width = c.stringWidth(date_text, "Helvetica", 14)
        x = (self.page_width - date_width) / 2
        c.drawString(x, y_position, date_text)

        return y_position - 20 * mm

    def _draw_signature_area(self, c: "canvas.Canvas") -> None:
        """
        Rysuje miejsce na podpisy

        Args:
            c (canvas.Canvas): Obiekt canvas ReportLab
        """
        y_position = self.margin + 30 * mm

        # Dwa obszary na podpisy
        signature_width = 70 * mm
        signature_y = y_position + 10 * mm

        # Lewy podpis (Organizator)
        left_x = self.page_width / 2 - signature_width - 20 * mm
        c.setStrokeColor(colors.HexColor('#333333'))
        c.setLineWidth(1)
        c.line(left_x, signature_y, left_x + signature_width, signature_y)

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor('#777777'))
        text = "Organizator"
        text_width = c.stringWidth(text, "Helvetica", 10)
        c.drawString(left_x + (signature_width - text_width) / 2, signature_y - 5 * mm, text)

        # Prawy podpis (Prowadzący)
        right_x = self.page_width / 2 + 20 * mm
        c.line(right_x, signature_y, right_x + signature_width, signature_y)

        text = "Prowadzący"
        text_width = c.stringWidth(text, "Helvetica", 10)
        c.drawString(right_x + (signature_width - text_width) / 2, signature_y - 5 * mm, text)

    def generate_certificate(
        self,
        participant_data: Dict[str, str],
        output_path: str
    ) -> bool:
        """
        Generuje certyfikat PDF dla uczestnika

        Args:
            participant_data (Dict[str, str]): Słownik z danymi uczestnika
                - imie: Imię uczestnika
                - nazwisko: Nazwisko uczestnika
                - warsztat: Nazwa warsztatu
                - data: Data warsztatu
            output_path (str): Ścieżka do zapisu pliku PDF

        Returns:
            bool: True jeśli sukces, False w przypadku błędu

        Example:
            >>> generator = CertificateGenerator()
            >>> data = {
            >>>     'imie': 'Jan',
            >>>     'nazwisko': 'Kowalski',
            >>>     'warsztat': 'Python',
            >>>     'data': '2025-01-15'
            >>> }
            >>> generator.generate_certificate(data, 'certyfikat.pdf')
        """
        try:
            # Utwórz katalog jeśli nie istnieje
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

            # Utwórz canvas
            c = canvas.Canvas(output_path, pagesize=landscape(A4))

            # Ustaw metadane PDF
            c.setAuthor("Certyfikator")
            c.setTitle(f"Certyfikat - {participant_data.get('imie', '')} {participant_data.get('nazwisko', '')}")
            c.setSubject(f"Certyfikat ukończenia: {participant_data.get('warsztat', '')}")

            # Konfiguruj czcionki
            self._setup_fonts(c)

            # Rysuj elementy certyfikatu
            self._draw_decorative_border(c)

            # Pozycja startowa (od góry)
            y_position = self.page_height - self.margin - 30 * mm

            # Logo (jeśli istnieje)
            logo_height = self._draw_logo(c)
            y_position -= logo_height

            # Tytuł
            y_position = self._draw_title(c, y_position)

            # Informacje o uczestniku
            y_position = self._draw_participant_info(c, participant_data, y_position)

            # Miejsce na podpisy
            self._draw_signature_area(c)

            # Zapisz PDF
            c.showPage()
            c.save()

            return True

        except Exception as e:
            print(f"Błąd podczas generowania certyfikatu: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_batch(
        self,
        participants_list: List[Dict[str, str]],
        output_dir: str,
        show_progress: bool = True
    ) -> Tuple[List[str], int, int]:
        """
        Generuje certyfikaty dla wielu uczestników

        Args:
            participants_list (List[Dict[str, str]]): Lista słowników z danymi uczestników
            output_dir (str): Katalog wyjściowy dla certyfikatów
            show_progress (bool): Czy wyświetlać pasek postępu

        Returns:
            Tuple[List[str], int, int]: (lista_plików, liczba_sukcesów, liczba_błędów)

        Example:
            >>> generator = CertificateGenerator()
            >>> participants = [
            >>>     {'imie': 'Jan', 'nazwisko': 'Kowalski', 'warsztat': 'Python', 'data': '2025-01-15'},
            >>>     {'imie': 'Anna', 'nazwisko': 'Nowak', 'warsztat': 'Python', 'data': '2025-01-15'}
            >>> ]
            >>> files, success, errors = generator.generate_batch(participants, 'output')
            >>> print(f"Wygenerowano {success} certyfikatów")
        """
        success_count = 0
        error_count = 0
        generated_files = []

        # Upewnij się, że katalog wyjściowy istnieje
        os.makedirs(output_dir, exist_ok=True)

        total = len(participants_list)

        for i, participant in enumerate(participants_list, 1):
            # Generuj nazwę pliku
            nazwisko = participant.get('nazwisko', 'Unknown').replace(' ', '_')
            imie = participant.get('imie', 'Unknown').replace(' ', '_')
            filename = f"Certyfikat_{nazwisko}_{imie}.pdf"
            output_path = os.path.join(output_dir, filename)

            # Wyświetl progress
            if show_progress:
                print(f"Generowanie [{i}/{total}]: {imie} {nazwisko}...")

            # Generuj certyfikat
            if self.generate_certificate(participant, output_path):
                success_count += 1
                generated_files.append(output_path)
            else:
                error_count += 1

        if show_progress:
            print(f"\n✓ Wygenerowano: {success_count} certyfikatów")
            if error_count > 0:
                print(f"✗ Błędy: {error_count}")

        return generated_files, success_count, error_count

    def create_zip_archive(
        self,
        pdf_files: List[str],
        zip_name: str = "certyfikaty.zip"
    ) -> Optional[str]:
        """
        Pakuje wszystkie PDF-y do archiwum ZIP

        Args:
            pdf_files (List[str]): Lista ścieżek do plików PDF
            zip_name (str): Nazwa pliku ZIP

        Returns:
            Optional[str]: Ścieżka do utworzonego archiwum lub None w przypadku błędu

        Example:
            >>> generator = CertificateGenerator()
            >>> files, _, _ = generator.generate_batch(participants, 'output')
            >>> zip_path = generator.create_zip_archive(files, 'wszystkie_certyfikaty.zip')
            >>> print(f"Archiwum utworzone: {zip_path}")
        """
        try:
            # Jeśli zip_name nie zawiera ścieżki, zapisz w katalogu pierwszego PDF
            if not os.path.dirname(zip_name) and pdf_files:
                output_dir = os.path.dirname(pdf_files[0])
                zip_path = os.path.join(output_dir, zip_name)
            else:
                zip_path = zip_name

            # Utwórz archiwum ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for pdf_file in pdf_files:
                    if os.path.exists(pdf_file):
                        # Dodaj tylko nazwę pliku bez pełnej ścieżki
                        arcname = os.path.basename(pdf_file)
                        zipf.write(pdf_file, arcname=arcname)

            print(f"✓ Utworzono archiwum: {zip_path}")
            print(f"  Zawiera {len(pdf_files)} plików PDF")

            return zip_path

        except Exception as e:
            print(f"Błąd podczas tworzenia archiwum ZIP: {e}")
            return None
