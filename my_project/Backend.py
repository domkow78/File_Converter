import os
from datetime import datetime
import psutil
import sys  # Dodano do obsługi zakończenia programu

def get_pendrive_path():
    """
    Wykrywa pierwszy dostępny dysk wymienny (pendrive) w systemie.
    Zwraca ścieżkę do pendrive'a lub None, jeśli nie znaleziono.
    """
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:  # Sprawdza, czy dysk jest wymienny
            return partition.mountpoint  # Zwraca punkt montowania (np. "D:\\")
    return None

def setup_pendrive_directories():
    """
    Wykrywa pendrive i tworzy katalogi 'Source' i 'Target' na nim.
    Zwraca ścieżki do katalogów lub kończy działanie, jeśli pendrive nie został wykryty.
    """
    pendrive_path = get_pendrive_path()
    if pendrive_path:
        print(f"Pendrive detected at: {pendrive_path}")
        source_dir = os.path.join(pendrive_path, "Source")
        target_dir = os.path.join(pendrive_path, "Target")

        # Tworzenie katalogów, jeśli nie istnieją
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
            print(f"Source directory created at: {source_dir}")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f"Target directory created at: {target_dir}")

        return source_dir, target_dir
    else:
        raise RuntimeError("No pendrive detected. Please insert a pendrive.")

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

if __name__ == "__main__":
    try:
        source_dir, target_dir = setup_pendrive_directories()
    except RuntimeError as e:
        print(e)
        sys.exit(1)  # Zakończenie działania programu z kodem błędu