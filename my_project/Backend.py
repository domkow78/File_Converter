import os
from datetime import datetime

def modify_file(source_file, target_file):
    """
    Modyfikuje plik tekstowy, dodając datę systemową na początku pliku,
    i zapisuje zmodyfikowany plik w katalogu docelowym.
    """
    try:
        print(f"Reading from: {source_file}")
        with open(source_file, 'r', encoding='utf-8') as src:
            content = src.read()

        # Dodanie daty systemowej na początku pliku
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modified_content = f"Modified on: {current_date}\n\n{content}\n"

        print(f"Appending to: {target_file}")
        # Dopisywanie zmodyfikowanego pliku w katalogu docelowym
        with open(target_file, 'a', encoding='utf-8') as tgt:
            tgt.write(modified_content)

        return True, f"File '{os.path.basename(source_file)}' modified successfully."
    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error modifying file '{os.path.basename(source_file)}': {e}"