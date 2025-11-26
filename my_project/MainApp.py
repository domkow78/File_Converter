import streamlit as st
import os
import shutil

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

# Funkcja do konwersji plików
def convert_files(source_dir, target_dir):
    try:
        if not os.path.exists(source_dir):
            st.error("Source directory does not exist.")
            return
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Przykładowa akcja: kopiowanie plików z katalogu źródłowego do docelowego
        files = os.listdir(source_dir)
        if not files:
            st.warning("No files found in the source directory.")
            return

        for file in files:
            source_path = os.path.join(source_dir, file)
            target_path = os.path.join(target_dir, file)
            try:
                if os.path.isfile(source_path):
                    shutil.copy(source_path, target_path)
            except Exception as e:
                st.error(f"Failed to copy file: {file}. Error: {e}")

        st.success(f"Files have been successfully converted and saved to {target_dir}")
    except Exception as e:
        st.error(f"An error occurred during file conversion: {e}")

# Automatyczne tworzenie katalogów domyślnych
default_source_dir = os.path.join(os.getcwd(), "Source")
default_target_dir = os.path.join(os.getcwd(), "Converted")

try:
    if not os.path.exists(default_source_dir):
        os.makedirs(default_source_dir)
except Exception as e:
    st.error(f"Failed to create default source directory. Error: {e}")

try:
    if not os.path.exists(default_target_dir):
        os.makedirs(default_target_dir)
except Exception as e:
    st.error(f"Failed to create default target directory. Error: {e}")

# Interfejs użytkownika
st.title("Symana File Converter")

# Wybór katalogu źródłowego
st.markdown("### Select Source Directory")
source_dir = st.text_input("Source Directory", value=default_source_dir, key="source_dir")

# Wyświetlenie plików w katalogu źródłowym
st.markdown("### Files in Source Directory")
try:
    if os.path.exists(source_dir):
        source_files = os.listdir(source_dir)
        if source_files:
            st.table({"Files": source_files})
        else:
            st.info("No files found in the source directory.")
    else:
        st.error("Source directory does not exist.")
except Exception as e:
    st.error(f"Failed to read source directory. Error: {e}")

# Wybór katalogu docelowego
st.markdown("### Select Target Directory")
target_dir = st.text_input("Target Directory", value=default_target_dir, key="target_dir")

# Wyświetlenie plików w katalogu docelowym
st.markdown("### Files in Target Directory")
try:
    if os.path.exists(target_dir):
        target_files = os.listdir(target_dir)
        if target_files:
            st.table({"Files": target_files})
        else:
            st.info("No files found in the target directory.")
    else:
        st.error("Target directory does not exist.")
except Exception as e:
    st.error(f"Failed to read target directory. Error: {e}")

# Przycisk "Convert"
if st.button("Convert"):
    convert_files(source_dir, target_dir)