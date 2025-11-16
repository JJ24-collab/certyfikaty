"""
Moduł do zarządzania szablonami certyfikatów
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional


class TemplateManager:
    """Klasa do zarządzania szablonami HTML certyfikatów"""

    def __init__(self, templates_dir='templates'):
        """
        Inicjalizacja managera szablonów

        Args:
            templates_dir (str): Katalog z szablonami
        """
        self.templates_dir = templates_dir
        self.templates_cache = {}  # Cache dla wczytanych szablonów

    def get_available_templates(self):
        """
        Zwraca listę dostępnych szablonów

        Returns:
            list: Lista nazw plików szablonów
        """
        if not os.path.exists(self.templates_dir):
            return []

        templates = []
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.html'):
                templates.append(filename)

        return sorted(templates)

    def get_template_path(self, template_name):
        """
        Zwraca pełną ścieżkę do szablonu

        Args:
            template_name (str): Nazwa szablonu

        Returns:
            str: Pełna ścieżka do pliku szablonu
        """
        return os.path.join(self.templates_dir, template_name)

    def load_template(self, template_name):
        """
        Wczytuje zawartość szablonu

        Args:
            template_name (str): Nazwa szablonu

        Returns:
            str: Zawartość szablonu lub None w przypadku błędu
        """
        template_path = self.get_template_path(template_name)

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()

        except Exception as e:
            print(f"Błąd podczas wczytywania szablonu: {e}")
            return None

    def save_template(self, template_name, content):
        """
        Zapisuje szablon

        Args:
            template_name (str): Nazwa szablonu
            content (str): Zawartość szablonu

        Returns:
            bool: True jeśli sukces, False w przypadku błędu
        """
        # Upewnij się, że katalog istnieje
        os.makedirs(self.templates_dir, exist_ok=True)

        template_path = self.get_template_path(template_name)

        try:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        except Exception as e:
            print(f"Błąd podczas zapisywania szablonu: {e}")
            return False

    def create_template_from_scratch(self, template_name, title, custom_css=''):
        """
        Tworzy nowy szablon od podstaw

        Args:
            template_name (str): Nazwa szablonu
            title (str): Tytuł certyfikatu
            custom_css (str): Dodatkowy CSS

        Returns:
            bool: True jeśli sukces, False w przypadku błędu
        """
        template_content = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: A4 landscape;
            margin: 0;
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: 'Georgia', serif;
        }}

        .certificate {{
            width: 297mm;
            height: 210mm;
            padding: 20mm;
            box-sizing: border-box;
            border: 10px solid #333;
            background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
            position: relative;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .title {{
            font-size: 48px;
            color: #333;
            margin-bottom: 20px;
        }}

        .content {{
            text-align: center;
            margin: 40px 0;
        }}

        .participant-name {{
            font-size: 36px;
            font-weight: bold;
            color: #000;
            margin: 20px 0;
        }}

        .workshop-info {{
            font-size: 24px;
            color: #555;
            margin: 20px 0;
        }}

        {custom_css}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="header">
            <h1 class="title">{title}</h1>
        </div>

        <div class="content">
            <p class="workshop-info">Niniejszym poświadcza się, że</p>
            <h2 class="participant-name">{{imie}} {{nazwisko}}</h2>
            <p class="workshop-info">ukończył/a warsztat</p>
            <h3 class="workshop-info">{{warsztat}}</h3>
            <p class="workshop-info">w dniu {{data}}</p>
        </div>
    </div>
</body>
</html>"""

        return self.save_template(template_name, template_content)

    def delete_template(self, template_name):
        """
        Usuwa szablon

        Args:
            template_name (str): Nazwa szablonu

        Returns:
            bool: True jeśli sukces, False w przypadku błędu
        """
        template_path = self.get_template_path(template_name)

        try:
            if os.path.exists(template_path):
                os.remove(template_path)
                # Usuń z cache
                if template_name in self.templates_cache:
                    del self.templates_cache[template_name]
                return True
            return False

        except Exception as e:
            print(f"Błąd podczas usuwania szablonu: {e}")
            return False

    def load_templates(self) -> Dict[str, str]:
        """
        Skanuje folder templates/ i wczytuje wszystkie szablony

        Returns:
            Dict[str, str]: Słownik {nazwa_szablonu: zawartość_html}
        """
        templates = {}
        available = self.get_available_templates()

        for template_name in available:
            content = self.load_template(template_name)
            if content:
                templates[template_name] = content
                self.templates_cache[template_name] = content

        return templates

    def apply_template(self, template_name: str, data: Dict[str, str]) -> Optional[str]:
        """
        Renderuje szablon z danymi (zastępuje placeholdery)

        Args:
            template_name (str): Nazwa szablonu
            data (Dict[str, str]): Dane do wstawienia, np.:
                {
                    'imie': 'Jan',
                    'nazwisko': 'Kowalski',
                    'warsztat': 'Python dla początkujących',
                    'data': '2024-01-15',
                    'organizacja': 'NGO XYZ',
                    'logo_path': 'path/to/logo.png'
                }

        Returns:
            str: Wyrenderowany HTML lub None w przypadku błędu

        Example:
            >>> manager = TemplateManager()
            >>> data = {
            ...     'imie': 'Jan',
            ...     'nazwisko': 'Kowalski',
            ...     'warsztat': 'Python',
            ...     'data': '2024-01-15',
            ...     'organizacja': 'Moja Organizacja'
            ... }
            >>> html = manager.apply_template('szablon_podstawowy.html', data)
            >>> print(html[:100])
        """
        # Wczytaj szablon (z cache lub z pliku)
        if template_name in self.templates_cache:
            template_content = self.templates_cache[template_name]
        else:
            template_content = self.load_template(template_name)
            if not template_content:
                return None
            self.templates_cache[template_name] = template_content

        # Zastąp placeholdery
        rendered = template_content

        # Podstawowe placeholdery
        placeholders = {
            '{{imie}}': data.get('imie', data.get('Imię', '')),
            '{{nazwisko}}': data.get('nazwisko', data.get('Nazwisko', '')),
            '{{warsztat}}': data.get('warsztat', data.get('Warsztat', '')),
            '{{data}}': data.get('data', data.get('Data', '')),
            '{{organizacja}}': data.get('organizacja', 'Organizacja'),
            '{{logo_path}}': data.get('logo_path', ''),
        }

        # Zastąp wszystkie placeholdery
        for placeholder, value in placeholders.items():
            rendered = rendered.replace(placeholder, str(value))

        # Obsługa logo - jeśli brak logo_path, usuń tag <img>
        if not data.get('logo_path'):
            # Usuń cały tag <img> z logo
            rendered = re.sub(
                r'<img[^>]*class="logo"[^>]*>',
                '',
                rendered,
                flags=re.IGNORECASE
            )

        return rendered

    def get_template_metadata(self, template_name: str) -> Dict[str, str]:
        """
        Wyciąga metadane szablonu (nazwa, opis, styl)

        Args:
            template_name (str): Nazwa szablonu

        Returns:
            Dict[str, str]: Metadane szablonu
        """
        # Mapowanie nazw szablonów na metadane
        templates_info = {
            'szablon_podstawowy.html': {
                'display_name': 'Podstawowy',
                'description': 'Minimalistyczny, elegancki szablon',
                'style': 'elegant',
                'color': '#2c3e50'
            },
            'szablon_kolorowy.html': {
                'display_name': 'Kolorowy',
                'description': 'Żywy szablon z kolorową ramką',
                'style': 'playful',
                'color': '#e74c3c'
            },
            'szablon_formalny.html': {
                'display_name': 'Formalny',
                'description': 'Bardzo oficjalny, klasyczny styl',
                'style': 'formal',
                'color': '#34495e'
            },
            'certificate_template.html': {
                'display_name': 'Klasyczny',
                'description': 'Domyślny szablon certyfikatu',
                'style': 'classic',
                'color': '#3498db'
            }
        }

        return templates_info.get(
            template_name,
            {
                'display_name': template_name.replace('.html', '').replace('_', ' ').title(),
                'description': 'Niestandardowy szablon',
                'style': 'custom',
                'color': '#95a5a6'
            }
        )
