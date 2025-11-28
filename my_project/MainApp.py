import streamlit as st
import os
from Backend import setup_pendrive_directories, modify_file

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

# Wyświetlenie katalogów
st.markdown(f"### Source Directory: {source_dir}")
st.markdown(f"### Target Directory: {target_dir}")

# Przycisk do konwersji
if st.button("Convert"):
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    if not files:
        st.warning("No files found in the source directory.")
    else:
        for file in files:
            source_file = os.path.join(source_dir, file)
            target_file = os.path.join(target_dir, file)

            # Wywołanie funkcji modyfikującej plik
            success, message = modify_file(source_file, target_file)
            if success:
                st.success(message)
            else:
                st.error(message)