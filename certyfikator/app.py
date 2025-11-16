"""
🎓 Certyfikator - Generator Certyfikatów
Aplikacja dla organizacji pozarządowych
"""

import streamlit as st
import pandas as pd
import os
from io import BytesIO
from modules import CertificateGenerator, DataHandler

# Konfiguracja strony
st.set_page_config(
    page_title="Certyfikator - Generator Certyfikatów",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicjalizacja session state
if 'generated_count' not in st.session_state:
    st.session_state.generated_count = 0
if 'current_files' not in st.session_state:
    st.session_state.current_files = []
if 'logo_uploaded' not in st.session_state:
    st.session_state.logo_uploaded = False


def init_session_state():
    """Inicjalizuje zmienne session state"""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'participants' not in st.session_state:
        st.session_state.participants = []


def show_header():
    """Wyświetla nagłówek aplikacji"""
    col1, col2 = st.columns([1, 4])

    with col1:
        # Sprawdź czy istnieje logo
        logo_path = 'assets/logo.png'
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)
        else:
            st.markdown("# 🎓")

    with col2:
        st.title("Certyfikator - Generator Certyfikatów")
        st.markdown("### 📋 Dla organizacji pozarządowych")

    st.markdown("---")


def show_sidebar():
    """Wyświetla sidebar z informacjami"""
    with st.sidebar:
        st.markdown("## ℹ️ Informacje")

        st.info("""
        **Certyfikator** to aplikacja do automatycznego generowania
        profesjonalnych certyfikatów dla uczestników warsztatów i szkoleń.
        """)

        st.markdown("---")

        # Statystyki sesji
        st.markdown("## 📊 Statystyki sesji")
        st.metric(
            "Certyfikaty wygenerowane",
            st.session_state.generated_count,
            delta=None
        )

        if st.session_state.current_files:
            st.metric(
                "Pliki w ostatniej operacji",
                len(st.session_state.current_files)
            )

        st.markdown("---")

        # Informacje o autorze i wersji
        st.markdown("## 👨‍💻 O aplikacji")
        st.markdown("""
        **Wersja:** 1.0.0
        **Autor:** Certyfikator Team
        **Licencja:** MIT

        **Funkcje:**
        - ✅ Generowanie PDF
        - ✅ Obsługa CSV/Excel
        - ✅ Edycja danych
        - ✅ Podgląd certyfikatów
        - ✅ Eksport do ZIP
        """)

        st.markdown("---")

        # Reset statystyk
        if st.button("🔄 Resetuj statystyki", use_container_width=True):
            st.session_state.generated_count = 0
            st.session_state.current_files = []
            st.rerun()


def download_example_csv():
    """Tworzy przykładowy plik CSV do pobrania"""
    example_data = {
        'Imię': ['Jan', 'Anna', 'Piotr'],
        'Nazwisko': ['Kowalski', 'Nowak', 'Wiśniewski'],
        'Warsztat': ['Python dla początkujących', 'Python dla początkujących', 'Python dla początkujących'],
        'Data': ['2025-01-15', '2025-01-15', '2025-01-15'],
        'Email': ['jan@example.com', 'anna@example.com', 'piotr@example.com']
    }

    df = pd.DataFrame(example_data)
    return df.to_csv(index=False).encode('utf-8')


def tab_generate_certificates():
    """TAB 1: Generowanie certyfikatów"""

    st.header("📝 Generuj Certyfikaty")

    # Sekcja 1: Upload pliku
    st.subheader("1️⃣ Wczytaj dane uczestników")

    # Instrukcja
    with st.expander("📖 Jak przygotować plik?", expanded=False):
        st.markdown("""
        **Wymagane kolumny:**
        - `Imię` - Imię uczestnika
        - `Nazwisko` - Nazwisko uczestnika
        - `Warsztat` - Nazwa warsztatu/szkolenia
        - `Data` - Data warsztatu (np. 2025-01-15)

        **Opcjonalne kolumny:**
        - `Email` - Adres email uczestnika

        **Obsługiwane formaty:** CSV, XLSX, XLS
        """)

    col1, col2 = st.columns([3, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Wybierz plik CSV lub Excel",
            type=['csv', 'xlsx', 'xls'],
            help="Plik musi zawierać kolumny: Imię, Nazwisko, Warsztat, Data"
        )

    with col2:
        st.download_button(
            label="⬇️ Pobierz przykład",
            data=download_example_csv(),
            file_name="example_participants.csv",
            mime="text/csv",
            use_container_width=True
        )

    if uploaded_file is None:
        st.info("👆 Wczytaj plik z danymi uczestników, aby rozpocząć")
        return

    # Wczytanie i walidacja danych
    try:
        # Zapisz tymczasowo
        temp_path = os.path.join('data', f'temp_{uploaded_file.name}')
        os.makedirs('data', exist_ok=True)

        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Wczytaj dane
        handler = DataHandler()
        df = handler.load_participants(temp_path)

        st.success(f"✅ Wczytano {len(df)} rekordów")

        # Statystyki
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Uczestników", len(df))
        col2.metric("📋 Kolumn", len(df.columns))

        # Unikalne warsztaty
        unique_workshops = df['Warsztat'].nunique() if 'Warsztat' in df.columns else 0
        col3.metric("🎯 Warsztatów", unique_workshops)

        st.markdown("---")

        # Sekcja 2: Edycja danych
        st.subheader("2️⃣ Podgląd i edycja danych")

        # Edytowalna tabela
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="data_editor"
        )

        st.session_state.df = edited_df

        # Walidacja danych
        st.markdown("---")
        st.subheader("3️⃣ Walidacja danych")

        errors = handler.validate_data(edited_df)

        if errors:
            st.error("⚠️ Znaleziono problemy w danych:")
            for error in errors:
                st.warning(f"• {error}")

            if not st.checkbox("✅ Kontynuuj mimo ostrzeżeń"):
                st.stop()
        else:
            st.success("✅ Wszystkie dane są poprawne!")

        # Sekcja 3.5: Wybór szablonu
        st.markdown("---")
        st.subheader("4️⃣ Wybór szablonu certyfikatu")

        from modules.template_manager import TemplateManager

        template_manager = TemplateManager('templates')
        available_templates = template_manager.get_available_templates()

        if not available_templates:
            st.warning("⚠️ Nie znaleziono szablonów w folderze templates/")
            available_templates = []

        col1, col2 = st.columns([2, 1])

        with col1:
            # Selectbox wyboru szablonu
            template_options = []
            template_display = {}

            for template_name in available_templates:
                metadata = template_manager.get_template_metadata(template_name)
                display = f"{metadata['display_name']} - {metadata['description']}"
                template_options.append(display)
                template_display[display] = template_name

            selected_display = st.selectbox(
                "📄 Wybierz szablon:",
                template_options if template_options else ["Brak dostępnych szablonów"],
                help="Wybierz styl certyfikatu"
            )

            selected_template = template_display.get(selected_display, available_templates[0] if available_templates else None)

        with col2:
            # Upload własnego szablonu
            custom_template = st.file_uploader(
                "📤 Lub wgraj własny szablon HTML",
                type=['html'],
                help="Szablon musi zawierać placeholdery: {{imie}}, {{nazwisko}}, {{warsztat}}, {{data}}, {{organizacja}}"
            )

            if custom_template:
                # Zapisz custom template
                custom_path = os.path.join('templates', 'custom_template.html')
                os.makedirs('templates', exist_ok=True)

                with open(custom_path, 'wb') as f:
                    f.write(custom_template.getbuffer())

                selected_template = 'custom_template.html'
                st.success("✅ Własny szablon wczytany!")

        # Podgląd szablonu (miniaturka)
        if selected_template:
            with st.expander("👁️ Podgląd szablonu", expanded=False):
                metadata = template_manager.get_template_metadata(selected_template)

                col_a, col_b = st.columns([1, 2])

                with col_a:
                    # Badge ze stylem
                    style_colors = {
                        'elegant': '#2c3e50',
                        'playful': '#e74c3c',
                        'formal': '#34495e',
                        'classic': '#3498db',
                        'custom': '#95a5a6'
                    }

                    color = style_colors.get(metadata['style'], '#95a5a6')

                    st.markdown(f"""
                    <div style="padding: 20px; background: {color}; color: white; border-radius: 10px; text-align: center;">
                        <h3 style="margin:0; color: white;">{metadata['display_name']}</h3>
                        <p style="margin:5px 0; font-size: 14px;">{metadata['description']}</p>
                        <p style="margin:5px 0; font-size: 12px; opacity: 0.8;">Styl: {metadata['style']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_b:
                    # Przykładowy render (z placeholder danymi)
                    example_data = {
                        'imie': 'Jan',
                        'nazwisko': 'Kowalski',
                        'warsztat': 'Python dla początkujących',
                        'data': '2024-01-15',
                        'organizacja': 'Twoja Organizacja'
                    }

                    preview_html = template_manager.apply_template(selected_template, example_data)
                    if preview_html:
                        # Renderuj HTML w mini podglądzie (CSS scale down)
                        scaled_html = f"""
                        <div style="transform: scale(0.25); transform-origin: top left; width: 400%; height: 300px; overflow: hidden; border: 2px solid #ddd; border-radius: 5px;">
                            {preview_html}
                        </div>
                        """
                        st.markdown(scaled_html, unsafe_allow_html=True)
                    else:
                        st.error("Nie można wczytać podglądu szablonu")

        # Zapisz wybrany szablon w session state
        st.session_state.selected_template = selected_template

        # Sekcja 4: Konfiguracja certyfikatu
        st.markdown("---")
        st.subheader("5️⃣ Konfiguracja certyfikatu")

        col1, col2 = st.columns(2)

        with col1:
            org_name = st.text_input(
                "📌 Nazwa organizacji",
                value="Fundacja Edukacja",
                help="Nazwa organizacji wystawiającej certyfikat"
            )

            signer_name = st.text_input(
                "✍️ Osoba podpisująca",
                value="Jan Kowalski",
                help="Imię i nazwisko osoby podpisującej certyfikat"
            )

        with col2:
            signer_position = st.text_input(
                "💼 Stanowisko",
                value="Prezes Zarządu",
                help="Stanowisko osoby podpisującej"
            )

            # Upload logo
            logo_file = st.file_uploader(
                "🖼️ Logo organizacji (opcjonalnie)",
                type=['png', 'jpg', 'jpeg'],
                help="Zalecaný rozmiar: 400x400 pikseli"
            )

        # Zapisz logo jeśli wgrane
        logo_path = None
        if logo_file is not None:
            logo_path = 'assets/temp_logo.png'
            os.makedirs('assets', exist_ok=True)

            with open(logo_path, 'wb') as f:
                f.write(logo_file.getbuffer())

            st.session_state.logo_uploaded = True
            st.success("✅ Logo wczytane")
        elif os.path.exists('assets/logo.png'):
            logo_path = 'assets/logo.png'

        # Sekcja 5: Podgląd
        st.markdown("---")
        st.subheader("6️⃣ Podgląd certyfikatu")

        col1, col2 = st.columns([2, 1])

        with col1:
            if len(edited_df) > 0:
                # Wybór uczestnika do podglądu
                preview_options = [
                    f"{row['Imię']} {row['Nazwisko']}"
                    for _, row in edited_df.iterrows()
                ]

                selected_participant_idx = st.selectbox(
                    "Wybierz uczestnika do podglądu:",
                    range(len(preview_options)),
                    format_func=lambda x: preview_options[x]
                )

        with col2:
            if st.button("👁️ Wygeneruj podgląd", type="secondary", use_container_width=True):
                with st.spinner("Generowanie podglądu..."):
                    try:
                        # Przygotuj dane uczestnika
                        row = edited_df.iloc[selected_participant_idx]
                        participant = {
                            'imie': row['Imię'],
                            'nazwisko': row['Nazwisko'],
                            'warsztat': row['Warsztat'],
                            'data': str(row['Data']),
                            'organizacja': org_name
                        }

                        # Generuj certyfikat z wybranym szablonem
                        if selected_template:
                            # Użyj PDFGenerator z szablonem HTML (WeasyPrint)
                            from modules.pdf_generator import PDFGenerator
                            generator = PDFGenerator(template_name=selected_template, templates_dir='templates')
                        else:
                            # Fallback - użyj CertificateGenerator (ReportLab)
                            generator = CertificateGenerator(logo_path=logo_path)

                        preview_path = 'output/preview.pdf'
                        os.makedirs('output', exist_ok=True)

                        if generator.generate_certificate(participant, preview_path):
                            with open(preview_path, 'rb') as f:
                                st.download_button(
                                    label="⬇️ Pobierz podgląd",
                                    data=f.read(),
                                    file_name=f"Podglad_{participant['nazwisko']}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            st.success("✅ Podgląd wygenerowany!")
                        else:
                            st.error("❌ Błąd podczas generowania podglądu")

                    except Exception as e:
                        st.error(f"❌ Błąd: {e}")
                        import traceback
                        st.code(traceback.format_exc())

        # Sekcja 6: Generowanie masowe
        st.markdown("---")
        st.subheader("7️⃣ Generowanie masowe")

        st.info(f"📊 Zostanie wygenerowanych **{len(edited_df)}** certyfikatów z szablonem **{template_manager.get_template_metadata(selected_template)['display_name']}**")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            if st.button("🚀 Generuj wszystkie certyfikaty", type="primary", use_container_width=True):
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # Przygotuj dane
                    participants = handler.get_participants_list(edited_df)

                    # Dodaj organizację do wszystkich uczestników
                    for p in participants:
                        p['organizacja'] = org_name

                    # Generuj certyfikaty z wybranym szablonem
                    if selected_template:
                        from modules.pdf_generator import PDFGenerator
                        generator = PDFGenerator(template_name=selected_template, templates_dir='templates')
                    else:
                        # Fallback do ReportLab
                        generator = CertificateGenerator(logo_path=logo_path)

                    os.makedirs('output', exist_ok=True)

                    generated_files = []
                    success_count = 0
                    error_count = 0

                    total = len(participants)

                    for i, participant in enumerate(participants, 1):
                        # Update progress
                        progress = i / total
                        progress_bar.progress(progress)
                        status_text.text(f"Generowanie [{i}/{total}]: {participant['imie']} {participant['nazwisko']}...")

                        # Generuj certyfikat
                        nazwisko = participant.get('nazwisko', 'Unknown').replace(' ', '_')
                        imie = participant.get('imie', 'Unknown').replace(' ', '_')
                        filename = f"Certyfikat_{nazwisko}_{imie}.pdf"
                        output_path = os.path.join('output', filename)

                        if generator.generate_certificate(participant, output_path):
                            generated_files.append(output_path)
                            success_count += 1
                        else:
                            error_count += 1

                    # Utwórz archiwum ZIP
                    status_text.text("Tworzenie archiwum ZIP...")

                    # Użyj CertificateGenerator.create_zip_archive() lub stwórz ZIP ręcznie
                    import zipfile
                    zip_path = os.path.join('output', 'certyfikaty.zip')

                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for file in generated_files:
                            zipf.write(file, os.path.basename(file))

                    status_text.text("✅ Gotowe!")

                    progress_bar.empty()
                    status_text.empty()

                    # Podsumowanie
                    st.success(f"✅ Wygenerowano {success_count} certyfikatów!")

                    if error_count > 0:
                        st.warning(f"⚠️ Błędy: {error_count}")

                    # Zapisz do session state
                    st.session_state.generated_count += success_count
                    st.session_state.current_files = generated_files

                    # Przycisk do pobrania ZIP
                    if zip_path and os.path.exists(zip_path):
                        with open(zip_path, 'rb') as f:
                            st.download_button(
                                label="📦 Pobierz wszystkie certyfikaty (ZIP)",
                                data=f.read(),
                                file_name="certyfikaty.zip",
                                mime="application/zip",
                                use_container_width=True
                            )

                        file_size = os.path.getsize(zip_path) / 1024
                        st.info(f"📁 Rozmiar archiwum: {file_size:.2f} KB")

                    # Lista wygenerowanych plików
                    with st.expander("📋 Lista wygenerowanych plików", expanded=True):
                        for i, file_path in enumerate(generated_files, 1):
                            filename = os.path.basename(file_path)
                            file_size = os.path.getsize(file_path) / 1024
                            st.text(f"{i}. {filename} ({file_size:.1f} KB)")

                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Błąd podczas generowania: {e}")
                    import traceback
                    with st.expander("🔍 Szczegóły błędu"):
                        st.code(traceback.format_exc())

    except FileNotFoundError as e:
        st.error(f"❌ Plik nie znaleziony: {e}")
    except ValueError as e:
        st.error(f"❌ Błąd walidacji: {e}")
        st.info("💡 Sprawdź czy plik zawiera wszystkie wymagane kolumny")
    except Exception as e:
        st.error(f"❌ Nieoczekiwany błąd: {e}")
        with st.expander("🔍 Szczegóły błędu"):
            import traceback
            st.code(traceback.format_exc())


def tab_instructions():
    """TAB 2: Instrukcja"""

    st.header("ℹ️ Instrukcja użytkowania")

    # Sekcja 1: Przygotowanie danych
    st.subheader("1️⃣ Jak przygotować plik z danymi?")

    st.markdown("""
    ### 📊 Format danych

    Plik CSV lub Excel musi zawierać następujące kolumny:

    | Kolumna | Wymagana | Opis | Przykład |
    |---------|----------|------|----------|
    | **Imię** | ✅ Tak | Imię uczestnika | Jan |
    | **Nazwisko** | ✅ Tak | Nazwisko uczestnika | Kowalski |
    | **Warsztat** | ✅ Tak | Nazwa warsztatu/szkolenia | Python dla początkujących |
    | **Data** | ✅ Tak | Data warsztatu | 2025-01-15 lub 15 stycznia 2025 |
    | **Email** | ❌ Nie | Adres email (opcjonalnie) | jan@example.com |

    ### 📝 Przykładowy plik CSV:

    ```csv
    Imię,Nazwisko,Warsztat,Data,Email
    Jan,Kowalski,Python dla początkujących,2025-01-15,jan@example.com
    Anna,Nowak,Python dla początkujących,2025-01-15,anna@example.com
    Piotr,Wiśniewski,Python dla początkujących,2025-01-15,piotr@example.com
    ```

    ### 💡 Wskazówki:
    - Używaj UTF-8 jako kodowania pliku
    - Możesz używać polskich znaków (ą, ć, ę, ł, ń, ó, ś, ź, ż)
    - Data może być w formacie: YYYY-MM-DD lub w formie tekstowej
    - Nie używaj znaków specjalnych w nazwach plików
    """)

    st.markdown("---")

    # Sekcja 2: Krok po kroku
    st.subheader("2️⃣ Proces generowania certyfikatów")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Krok 1: Wczytanie danych
        1. Przygotuj plik CSV lub Excel
        2. Kliknij "Wybierz plik"
        3. Sprawdź czy dane się wczytały poprawnie

        ### Krok 2: Edycja danych
        1. Sprawdź dane w tabeli
        2. Edytuj bezpośrednio w tabeli jeśli potrzeba
        3. Dodaj lub usuń wiersze

        ### Krok 3: Walidacja
        1. Aplikacja automatycznie sprawdzi dane
        2. Popraw ewentualne błędy
        3. Możesz kontynuować mimo ostrzeżeń
        """)

    with col2:
        st.markdown("""
        ### Krok 4: Konfiguracja
        1. Wpisz nazwę organizacji
        2. Podaj dane osoby podpisującej
        3. Opcjonalnie wgraj logo (PNG, JPG)

        ### Krok 5: Podgląd
        1. Wybierz uczestnika z listy
        2. Kliknij "Wygeneruj podgląd"
        3. Pobierz i sprawdź certyfikat

        ### Krok 6: Generowanie
        1. Kliknij "Generuj wszystkie certyfikaty"
        2. Poczekaj na zakończenie
        3. Pobierz archiwum ZIP z certyfikatami
        """)

    st.markdown("---")

    # Sekcja 3: FAQ
    st.subheader("❓ Najczęściej zadawane pytania (FAQ)")

    with st.expander("🤔 Jak dodać logo organizacji?"):
        st.markdown("""
        W sekcji "Konfiguracja certyfikatu" znajduje się opcja upload logo:
        1. Kliknij "Browse files" przy polu "Logo organizacji"
        2. Wybierz plik PNG lub JPG
        3. Zalecany rozmiar: 400x400 pikseli
        4. Logo pojawi się na górze certyfikatu
        """)

    with st.expander("📝 Jak edytować dane w tabeli?"):
        st.markdown("""
        Tabela jest w pełni edytowalna:
        - **Edycja:** Kliknij dwukrotnie na komórkę
        - **Dodanie wiersza:** Kliknij "+" na dole tabeli
        - **Usunięcie wiersza:** Zaznacz wiersz i kliknij "-"
        - **Kopiowanie:** Ctrl+C / Ctrl+V działa
        """)

    with st.expander("⚠️ Co oznaczają ostrzeżenia walidacji?"):
        st.markdown("""
        Aplikacja sprawdza:
        - **Puste wartości** - niektóre pola są puste
        - **Duplikaty** - ta sama osoba pojawia się więcej niż raz
        - **Format daty** - nieprawidłowy format daty
        - **Format email** - nieprawidłowy adres email

        Możesz kontynuować mimo ostrzeżeń, ale certyfikaty mogą być niepełne.
        """)

    with st.expander("📦 Jak pobrać wygenerowane certyfikaty?"):
        st.markdown("""
        Po wygenerowaniu certyfikatów:
        1. Kliknij przycisk "Pobierz wszystkie certyfikaty (ZIP)"
        2. Plik ZIP zostanie pobrany
        3. Rozpakuj archiwum
        4. Certyfikaty mają nazwy: `Certyfikat_Nazwisko_Imie.pdf`

        Możesz też pobrać pojedynczy certyfikat używając podglądu.
        """)

    with st.expander("🎨 Jak wygląda certyfikat?"):
        st.markdown("""
        Certyfikat ma następujący layout:
        - Format: A4 poziomy (landscape)
        - Ozdobna ramka z narożnikami
        - Logo organizacji (jeśli wgrane)
        - Tytuł "CERTYFIKAT"
        - Imię i nazwisko uczestnika (podkreślone)
        - Nazwa warsztatu
        - Data warsztatu
        - Miejsca na podpisy (Organizator, Prowadzący)

        Styl profesjonalny, kolory: niebieski i szary.
        """)

    with st.expander("💾 Gdzie zapisują się certyfikaty?"):
        st.markdown("""
        Certyfikaty są zapisywane w katalogu `output/`:
        - Pojedyncze pliki PDF
        - Archiwum ZIP ze wszystkimi certyfikatami

        Pliki nie są usuwane automatycznie. Możesz je usunąć ręcznie.
        """)

    with st.expander("🐛 Co zrobić gdy aplikacja nie działa?"):
        st.markdown("""
        Jeśli napotkasz problemy:

        1. **Sprawdź format danych** - czy plik ma wszystkie wymagane kolumny
        2. **Sprawdź kodowanie** - użyj UTF-8
        3. **Sprawdź rozmiar pliku** - bardzo duże pliki mogą powodować problemy
        4. **Odśwież aplikację** - naciśnij F5
        5. **Sprawdź logi** - szczegóły błędu są w expanderze "Szczegóły błędu"

        Jeśli problem się powtarza, skontaktuj się z administratorem.
        """)

    st.markdown("---")

    # Sekcja 4: Wsparcie
    st.subheader("📞 Wsparcie")

    st.info("""
    **Potrzebujesz pomocy?**

    - 📧 Email: support@certyfikator.pl
    - 📚 Dokumentacja: README.md w głównym katalogu
    - 🐛 Zgłoszenia błędów: GitHub Issues
    - 💡 Propozycje funkcji: GitHub Discussions
    """)

    # Przykładowy plik do pobrania
    st.markdown("---")
    st.subheader("📥 Pobierz przykładowy plik")

    st.download_button(
        label="⬇️ Pobierz example_participants.csv",
        data=download_example_csv(),
        file_name="example_participants.csv",
        mime="text/csv",
        use_container_width=False
    )


def main():
    """Główna funkcja aplikacji"""

    # Inicjalizacja
    init_session_state()

    # Header
    show_header()

    # Sidebar
    show_sidebar()

    # Główna zawartość - TABS
    tab1, tab2 = st.tabs(["📝 Generuj Certyfikaty", "ℹ️ Instrukcja"])

    with tab1:
        tab_generate_certificates()

    with tab2:
        tab_instructions()


if __name__ == "__main__":
    main()
