import streamlit as st
import os
from Backend import setup_pendrive_directories, check_required_files, modify_file

st.set_page_config(page_title="File Converter", layout="wide")

# Stylizacja CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} /* Ukrywa menu w górnym pasku */
    footer {visibility: hidden;}   /* Ukrywa stopkę */
    header {visibility: hidden;}   /* Ukrywa nagłówek Streamlit */
    .block-container {
        padding: 0.5rem 1rem;
        max-width: 100%;
        background-color: #000011; /* Czarny kolor */
    }
    </style>
""", unsafe_allow_html=True)

# Interfejs użytkownika
st.title("File Converter")

# Wykrywanie pendrive'a i ustawianie katalogów
try:
    source_dir, target_dir = setup_pendrive_directories()
    st.success(f"Pendrive detected. Source directory: {source_dir}, Target directory: {target_dir}")
except RuntimeError as e:
    st.error(str(e))
    st.stop()  # Zatrzymuje dalsze wykonywanie aplikacji

# Sprawdzanie wymaganych plików
zip_file_name, bsh_file_name = check_required_files(source_dir)

if zip_file_name and bsh_file_name:
    st.success("Both required files are present:")
    st.markdown(f"- ZIP file: `{zip_file_name}`")
    st.markdown(f"- BSH file: `{bsh_file_name}`")

    # Przycisk do konwersji
    if st.button("Convert"):
        st.info("Conversion process started...")
        # Wywołanie funkcji modify_file
        modify_file(zip_file_name, bsh_file_name)
        st.success("Conversion completed!")
elif not zip_file_name and not bsh_file_name:
    st.error("Both required files are missing: `.zip` file and `bsh-lc_domain`.")
elif not zip_file_name:
    st.error("Missing file: `.zip` file.")
elif not bsh_file_name:
    st.error("Missing file: `bsh-lc_domain`.")