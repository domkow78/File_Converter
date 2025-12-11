import os
from datetime import datetime
import psutil
import sys
import streamlit as st

def get_pendrive_path():
    """
    Wykrywa pierwszy dostępny dysk wymienny (pendrive) w systemie.
    Obsługuje systemy Windows i Linux (Ubuntu).
    Zwraca ścieżkę do pendrive'a lub None, jeśli nie znaleziono.
    """
    # Rozpoznanie systemu operacyjnego
    if os.name == 'nt':  # 'nt' oznacza Windows
        # Logika dla systemu Windows
        for partition in psutil.disk_partitions():
            print(f"Checking partition: {partition.device}, opts: {partition.opts}")  # Log diagnostyczny
            if 'removable' in partition.opts:  # Sprawdza, czy dysk jest wymienny
                return partition.mountpoint  # Zwraca punkt montowania (np. "D:\\")
    
    elif os.name == 'posix':  # 'posix' oznacza systemy uniksowe (Linux, macOS)
        # Logika dla systemu Linux
        media_dirs = ["/media", "/run/media"]
        for media_dir in media_dirs:
            if os.path.exists(media_dir):
                for user_dir in os.listdir(media_dir):
                    user_path = os.path.join(media_dir, user_dir)
                    if os.path.isdir(user_path):  # Sprawdza, czy to katalog
                        for device in os.listdir(user_path):
                            device_path = os.path.join(user_path, device)
                            if os.path.ismount(device_path):  # Sprawdza, czy to punkt montowania
                                print(f"Detected pendrive at: {device_path}")  # Log diagnostyczny
                                return device_path

    # Jeśli nie znaleziono pendrive'a
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
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return None, None

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
        st.success(f"Pendrive detected. Source directory: {source_dir}, Target directory: {target_dir}")
        print(f"Source directory: {source_dir}, Target directory: {target_dir}")  # Log diagnostyczny
    except RuntimeError as e:
        st.error(str(e))
        st.stop()