import os
from datetime import datetime
import psutil
import sys
import streamlit as st
import zipfile
import shutil
import subprocess
import platform

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

def modify_file(zip_file_name, bsh_file_name):
    if platform.system() == "Windows":
        raise RuntimeError("This function is not supported on Windows. Please use a Linux system.")
    
    """
    Modyfikuje pliki w katalogu Source i zapisuje wynik w katalogu Target.
    - Rozpakowuje plik .zip.
    - Modyfikuje obraz systemu plików SquashFS.
    - Podmienia plik bsh-lc_domain.
    - Zmienia uprawnienia pliku bsh-lc_domain na read, write, execute.
    - Pakuje zmodyfikowane pliki do nowego archiwum .zip w katalogu Target.
    """
    try:
        # Ścieżki do katalogów Source i Target
        source_dir = os.path.dirname(zip_file_name)
        target_dir = os.path.join(os.path.dirname(source_dir), "Target")
        os.makedirs(target_dir, exist_ok=True)

        # Rozpakowanie pliku .zip
        temp_extract_dir = os.path.join(source_dir, "temp_extracted")
        os.makedirs(temp_extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)
            print(f"ZIP file extracted to: {temp_extract_dir}")

        # Znalezienie pliku SquashFS i plików JSON
        squashfs_file = None
        for file in os.listdir(temp_extract_dir):
            if file.endswith(".squashfs"):
                squashfs_file = os.path.join(temp_extract_dir, file)
                break

        if not squashfs_file:
            raise FileNotFoundError("No SquashFS file found in the extracted ZIP.")

        # Rozpakowanie obrazu SquashFS
        squashfs_extract_dir = os.path.join(temp_extract_dir, "squashfs_extracted")
        os.makedirs(squashfs_extract_dir, exist_ok=True)
        subprocess.run(["unsquashfs", "-f", "-d", squashfs_extract_dir, squashfs_file], check=True)
        print(f"SquashFS file extracted to: {squashfs_extract_dir}")

        # Podmiana pliku bsh-lc_domain w katalogu usr/bin
        usr_bin_dir = os.path.join(squashfs_extract_dir, "usr", "bin")
        if not os.path.exists(usr_bin_dir):
            raise FileNotFoundError(f"Directory usr/bin not found in SquashFS image: {usr_bin_dir}")

        bsh_target_path = os.path.join(usr_bin_dir, "bsh-lc_domain")
        bsh_source_path = os.path.join(source_dir, bsh_file_name)
        shutil.copy(bsh_source_path, bsh_target_path)
        print(f"Replaced {bsh_target_path} with {bsh_source_path}")

        # Zmiana uprawnień pliku bsh-lc_domain na read, write, execute
        os.chmod(bsh_target_path, 0o755)
        print(f"Permissions for {bsh_target_path} set to read, write, execute.")

        # Spakowanie zmodyfikowanego obrazu SquashFS
        modified_squashfs_file = os.path.join(temp_extract_dir, "modified.squashfs")
        subprocess.run(["mksquashfs", squashfs_extract_dir, modified_squashfs_file], check=True)
        print(f"Modified SquashFS file created at: {modified_squashfs_file}")

        # Podmiana pliku SquashFS w katalogu tymczasowym
        shutil.copy(modified_squashfs_file, squashfs_file)

        # Spakowanie zmodyfikowanych plików do nowego ZIP
        modified_zip_file = os.path.join(target_dir, f"modified_{os.path.basename(zip_file_name)}")
        with zipfile.ZipFile(modified_zip_file, 'w') as zip_ref:
            for root, _, files in os.walk(temp_extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_extract_dir)
                    zip_ref.write(file_path, arcname)
        print(f"Modified ZIP file created at: {modified_zip_file}")

        # Usunięcie katalogu tymczasowego
        shutil.rmtree(temp_extract_dir)
        print(f"Temporary directory {temp_extract_dir} removed.")

        print("File modification completed successfully.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error during SquashFS processing: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        source_dir, target_dir = setup_pendrive_directories()
        st.success(f"Pendrive detected. Source directory: {source_dir}, Target directory: {target_dir}")
        print(f"Source directory: {source_dir}, Target directory: {target_dir}")  # Log diagnostyczny
    except RuntimeError as e:
        st.error(str(e))
        st.stop()