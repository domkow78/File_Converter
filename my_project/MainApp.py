import streamlit as st
import os
from Backend import modify_file

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

# Automatyczne tworzenie katalogów domyślnych
default_source_dir = os.path.join(os.getcwd(), "Source")
default_target_dir = os.path.join(os.getcwd(), "Target")

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

# Wybór katalogu docelowego
st.markdown("### Select Target Directory")
target_dir = st.text_input("Target Directory", value=default_target_dir, key="target_dir")

# Przycisk do konwersji
if st.button("Convert"):
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    if not os.path.exists(source_dir):
        st.error("Source directory does not exist.")
    elif not os.path.exists(target_dir):
        os.makedirs(target_dir)
        st.info(f"Target directory '{target_dir}' created.")

    # Pobranie listy plików z katalogu źródłowego
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    print(f"Files to process: {files}")
    if not files:
        st.warning("No files found in the source directory.")
    else:
        for file in files:
            source_file = os.path.join(source_dir, file)
            target_file = os.path.join(target_dir, file)

            # Wywołanie funkcji modyfikującej plik
            success, message = modify_file(source_file, target_file)
            print(message)
            if success:
                st.success(message)
            else:
                st.error(message)