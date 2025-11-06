"""
Certyfikator - Aplikacja do generowania certyfikatów
"""

import streamlit as st
import os
from modules import PDFGenerator, OCRProcessor, DataHandler, TemplateManager


# Konfiguracja strony
st.set_page_config(
    page_title="Certyfikator",
    page_icon="📜",
    layout="wide"
)


def main():
    """Główna funkcja aplikacji"""

    st.title("📜 Certyfikator")
    st.markdown("---")

    # Inicjalizacja obiektów
    template_manager = TemplateManager('templates')
    data_handler = DataHandler()
    ocr_processor = OCRProcessor()

    # Sidebar - menu nawigacji
    st.sidebar.title("Menu")
    menu = st.sidebar.radio(
        "Wybierz opcję:",
        ["Generuj certyfikaty", "Zarządzaj szablonami", "OCR listy obecności", "Informacje"]
    )

    if menu == "Generuj certyfikaty":
        generate_certificates_page(template_manager, data_handler)

    elif menu == "Zarządzaj szablonami":
        manage_templates_page(template_manager)

    elif menu == "OCR listy obecności":
        ocr_attendance_page(ocr_processor, data_handler)

    elif menu == "Informacje":
        info_page()


def generate_certificates_page(template_manager, data_handler):
    """Strona generowania certyfikatów"""

    st.header("Generuj certyfikaty")

    # Wybór szablonu
    templates = template_manager.get_available_templates()

    if not templates:
        st.warning("Brak dostępnych szablonów. Utwórz szablon w sekcji 'Zarządzaj szablonami'.")
        return

    selected_template = st.selectbox("Wybierz szablon:", templates)

    # Upload pliku z danymi
    st.subheader("1. Wczytaj dane uczestników")
    uploaded_file = st.file_uploader(
        "Wybierz plik CSV lub Excel z danymi uczestników",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file is not None:
        # Zapisz tymczasowo plik
        temp_path = os.path.join('data', 'temp_upload.csv' if uploaded_file.name.endswith('.csv') else 'temp_upload.xlsx')

        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        try:
            # Wczytaj dane uczestników
            df = data_handler.load_participants(temp_path)

            st.success(f"Wczytano {len(df)} rekordów")
            st.dataframe(df)

            # Walidacja danych
            st.subheader("2. Walidacja danych")
            errors = data_handler.validate_data(df)

            if errors:
                st.error("Znaleziono błędy w danych:")
                for error in errors:
                    st.warning(f"• {error}")

                # Pytaj użytkownika czy kontynuować mimo błędów
                if not st.checkbox("Kontynuuj mimo błędów"):
                    return
            else:
                st.success("✓ Wszystkie dane są poprawne")

            # Przycisk generowania
            st.subheader("3. Generuj certyfikaty")

            if st.button("Generuj wszystkie certyfikaty", type="primary"):
                with st.spinner("Generowanie certyfikatów..."):
                    # Pobierz listę uczestników
                    participants = data_handler.get_participants_list(df)

                    # Inicjalizuj generator PDF
                    template_path = template_manager.get_template_path(selected_template)
                    pdf_generator = PDFGenerator(template_path)

                    # Generuj certyfikaty
                    success, errors = pdf_generator.generate_batch(participants, 'output')

                    # Wyświetl wyniki
                    st.success(f"Wygenerowano {success} certyfikatów")

                    if errors > 0:
                        st.warning(f"Błędy: {errors}")

                    st.info(f"Certyfikaty zapisane w katalogu: output/")

        except FileNotFoundError as e:
            st.error(f"Błąd: {e}")
        except ValueError as e:
            st.error(f"Błąd walidacji: {e}")
        except Exception as e:
            st.error(f"Nieoczekiwany błąd: {e}")


def manage_templates_page(template_manager):
    """Strona zarządzania szablonami"""

    st.header("Zarządzaj szablonami")

    tab1, tab2, tab3 = st.tabs(["Podgląd szablonów", "Utwórz nowy szablon", "Edytuj szablon"])

    with tab1:
        st.subheader("Dostępne szablony")
        templates = template_manager.get_available_templates()

        if templates:
            for template in templates:
                with st.expander(f"📄 {template}"):
                    content = template_manager.load_template(template)
                    if content:
                        st.code(content, language='html')

                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if st.button(f"Usuń", key=f"delete_{template}"):
                                if template_manager.delete_template(template):
                                    st.success(f"Usunięto szablon: {template}")
                                    st.rerun()
                                else:
                                    st.error("Błąd podczas usuwania szablonu")
        else:
            st.info("Brak dostępnych szablonów")

    with tab2:
        st.subheader("Utwórz nowy szablon")

        template_name = st.text_input("Nazwa szablonu (z rozszerzeniem .html):")
        template_title = st.text_input("Tytuł certyfikatu:")

        custom_css = st.text_area("Dodatkowy CSS (opcjonalnie):", height=200)

        if st.button("Utwórz szablon"):
            if template_name and template_title:
                if not template_name.endswith('.html'):
                    template_name += '.html'

                if template_manager.create_template_from_scratch(
                    template_name, template_title, custom_css
                ):
                    st.success(f"Utworzono szablon: {template_name}")
                else:
                    st.error("Błąd podczas tworzenia szablonu")
            else:
                st.warning("Wypełnij wszystkie pola")

    with tab3:
        st.subheader("Edytuj szablon")

        templates = template_manager.get_available_templates()

        if templates:
            selected = st.selectbox("Wybierz szablon do edycji:", templates, key="edit_select")

            content = template_manager.load_template(selected)

            if content:
                new_content = st.text_area(
                    "Edytuj kod HTML:",
                    value=content,
                    height=400
                )

                if st.button("Zapisz zmiany"):
                    if template_manager.save_template(selected, new_content):
                        st.success("Zapisano zmiany")
                    else:
                        st.error("Błąd podczas zapisywania")
        else:
            st.info("Brak szablonów do edycji")


def ocr_attendance_page(ocr_processor, data_handler):
    """Strona OCR list obecności"""

    st.header("OCR list obecności")

    st.info("""
    Ta funkcja pozwala na wyciągnięcie imion i nazwisk z zeskanowanych list obecności.
    **Uwaga:** Wymaga zainstalowanego Tesseract OCR w systemie.
    """)

    uploaded_images = st.file_uploader(
        "Wybierz skany list obecności",
        type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
        accept_multiple_files=True
    )

    if uploaded_images:
        st.subheader("Przetwarzanie...")

        all_names = []

        for uploaded_image in uploaded_images:
            # Zapisz tymczasowo
            temp_path = os.path.join('data', 'attendance', uploaded_image.name)

            with open(temp_path, 'wb') as f:
                f.write(uploaded_image.getbuffer())

            # Przetwórz OCR
            with st.spinner(f"Przetwarzanie {uploaded_image.name}..."):
                names = ocr_processor.extract_names_from_attendance(temp_path)

                if names:
                    st.success(f"Znaleziono {len(names)} osób w pliku {uploaded_image.name}")

                    # Wyświetl znalezione nazwiska
                    for imie, nazwisko in names:
                        st.text(f"• {imie} {nazwisko}")
                        all_names.append((imie, nazwisko))
                else:
                    st.warning(f"Nie znaleziono danych w pliku {uploaded_image.name}")

        if all_names:
            st.subheader("Podsumowanie")
            st.write(f"Łącznie znaleziono {len(all_names)} osób")

            # Możliwość eksportu do CSV
            if st.button("Eksportuj do CSV"):
                import pandas as pd

                df = pd.DataFrame(all_names, columns=['Imię', 'Nazwisko'])
                csv_path = os.path.join('data', 'extracted_names.csv')
                df.to_csv(csv_path, index=False)

                st.success(f"Zapisano do: {csv_path}")


def info_page():
    """Strona informacyjna"""

    st.header("Informacje o aplikacji")

    st.markdown("""
    ## Certyfikator

    Aplikacja do automatycznego generowania certyfikatów dla uczestników warsztatów i szkoleń.

    ### Funkcje:
    - ✅ Generowanie certyfikatów PDF z szablonów HTML
    - ✅ Obsługa danych z plików CSV i Excel
    - ✅ OCR dla skanów list obecności
    - ✅ Zarządzanie szablonami certyfikatów
    - ✅ Wsadowe generowanie certyfikatów

    ### Wymagania:
    - Python 3.8+
    - Biblioteki z requirements.txt
    - Tesseract OCR (dla funkcji OCR)

    ### Struktura plików:
    ```
    certyfikator/
    ├── app.py                  # Główna aplikacja
    ├── modules/                # Moduły Python
    ├── templates/              # Szablony HTML
    ├── data/                   # Dane wejściowe
    └── output/                 # Wygenerowane certyfikaty
    ```

    ### Format danych wejściowych:
    Plik CSV lub Excel powinien zawierać następujące kolumny:
    - **Imię**: Imię uczestnika
    - **Nazwisko**: Nazwisko uczestnika
    - **Email**: Adres email
    - **Warsztat**: Nazwa warsztatu/szkolenia
    - **Data**: Data warsztatu

    ### Wsparcie:
    W razie problemów sprawdź dokumentację w pliku README.md
    """)


if __name__ == "__main__":
    main()
