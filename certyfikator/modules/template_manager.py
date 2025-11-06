"""
Moduł do zarządzania szablonami certyfikatów
"""

import os
from pathlib import Path


class TemplateManager:
    """Klasa do zarządzania szablonami HTML certyfikatów"""

    def __init__(self, templates_dir='templates'):
        """
        Inicjalizacja managera szablonów

        Args:
            templates_dir (str): Katalog z szablonami
        """
        self.templates_dir = templates_dir

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
                return True
            return False

        except Exception as e:
            print(f"Błąd podczas usuwania szablonu: {e}")
            return False
