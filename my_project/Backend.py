import os
from datetime import datetime
import psutil
import sys

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

def check_required_files(source_dir):
    """
    Sprawdza, czy w katalogu Source znajdują się dwa wymagane pliki:
    - Plik z rozszerzeniem .zip.
    - Plik o nazwie 'bsh-lc_domain'.
    Zwraca informacje o brakujących plikach oraz ich nazwy.
    """
    zip_file_name = None
    bsh_file_name = None

    for file in os.listdir(source_dir):
        if file.endswith(".zip"):  # Sprawdza, czy plik ma rozszerzenie .zip
            zip_file_name = file
        elif file == "bsh-lc_domain":  # Sprawdza, czy plik ma nazwę 'bsh-lc_domain'
            bsh_file_name = file

    return zip_file_name, bsh_file_name

def modify_file(source_file, target_file):
    """
    Tymczasowo pusta funkcja. Instrukcje zostaną dodane później.
    """
    print(f"Modify file called with: {source_file}, {target_file}")
    pass

if __name__ == "__main__":
    try:
        source_dir, target_dir = setup_pendrive_directories()
    except RuntimeError as e:
        print(e)
        sys.exit(1)  # Zakończenie działania programu z kodem błędu