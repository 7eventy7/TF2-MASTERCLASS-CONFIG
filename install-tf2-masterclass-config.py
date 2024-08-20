import os
import zipfile
import platform
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
import traceback
import winreg  # For Windows registry access

GITHUB_REPO_URL = "https://github.com/7eventy7/TF2-MASTERCLASS-CONFIG"
LATEST_RELEASE_URL = f"{GITHUB_REPO_URL}/releases/latest/download/TF2-MASTERCLASS-CONFIG.zip"

def display_startup_screen():
    print("=" * 70)
    print(" " * 20 + "TF2 MASTERCLASS CONFIG INSTALLER")
    print("=" * 70)
    print(" " * 25 + "v2.2.3 -- August 19th, 2024")
    print("=" * 70)
    print("\nThis script will help you install the TF2 Masterclass Config.")
    print("Please follow the instructions as prompted.\n")
    print("=" * 70 + "\n")

def get_steam_path():
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        return winreg.QueryValueEx(hkey, "InstallPath")[0]
    except:
        return None

def find_tf2_install_directory():
    system = platform.system()
    
    if system == "Windows":
        steam_path = get_steam_path()
        if steam_path:
            libraryfolders_path = Path(steam_path) / "steamapps" / "libraryfolders.vdf"
            if libraryfolders_path.exists():
                with open(libraryfolders_path, 'r') as f:
                    content = f.read()
                    library_paths = [Path(line.split('"')[-2]) for line in content.splitlines() if "path" in line]
                    library_paths.append(Path(steam_path))
                    
                    for library in library_paths:
                        tf2_path = library / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg"
                        if tf2_path.exists():
                            print(f"TF2 install directory found:\n\"{tf2_path}\"\n")
                            return tf2_path

        # If not found through Steam libraries, search all drives
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = Path(f"{drive}:")
            if drive_path.exists():
                standard_paths = [
                    drive_path / "Program Files (x86)" / "Steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg",
                    drive_path / "steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg"
                ]
                for path in standard_paths:
                    if path.exists():
                        print(f"TF2 install directory found:\n\"{path}\"\n")
                        return path
                
                try:
                    for root, dirs, _ in os.walk(drive_path):
                        if "steamapps" in dirs:
                            steam_path = Path(root) / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg"
                            if steam_path.exists():
                                print(f"TF2 install directory found:\n\"{steam_path}\"\n")
                                return steam_path
                except Exception:
                    pass
    elif system == "Darwin":  # macOS
        mac_path = Path.home() / "Library" / "Application Support" / "Steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg"
        if mac_path.exists():
            print(f"TF2 install directory found:\n\"{mac_path}\"\n")
            return mac_path
    elif system == "Linux":
        linux_paths = [
            Path.home() / ".steam" / "steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg",
            Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg"
        ]
        for path in linux_paths:
            if path.exists():
                print(f"TF2 install directory found:\n\"{path}\"\n")
                return path

    raise FileNotFoundError("TF2 install directory not found in any of the searched locations")

def download_latest_release(url):
    try:
        with urlopen(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file: {response.reason}")
            print("Downloaded latest release from GitHub\n")
            return BytesIO(response.read())
    except Exception as e:
        raise

def extract_cfg_files(zip_file, destination_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        cfg_files = [f for f in zip_ref.namelist() if f.endswith('.cfg')]
        zip_ref.extractall(path=destination_folder, members=cfg_files)
    print(f"Extracted .cfg files to:\n\"{destination_folder}\"\n")

def get_valid_input(prompt, valid_check, error_message):
    while True:
        user_input = input(prompt).strip()
        if valid_check(user_input):
            return user_input
        print(error_message)

def update_autoexec_cfg(destination_folder):
    autoexec_path = destination_folder / "autoexec.cfg"
    
    with autoexec_path.open('r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    
    # Prompt user for changes
    print("=" * 70)
    fps_limit = get_valid_input(
        "\n1. What is your desired fps limit?\nDefault: \"0\" - Disabled\nUser Input: (0 thru 1000)\nYour choice: ",
        lambda x: x.isdigit() and 0 <= int(x) <= 1000,
        "Unexpected input. Please enter a number between 0 and 1000."
    ) or "0"
    
    print("=" * 70)
    ptt_key = input("\n2. Change the push to talk keybind?\nDefault: \"INS\" - Insert\nUser Input: (Any single keybind)\nYour choice: ").strip() or "ins"
    
    print("=" * 70)
    swap_crouch = get_valid_input(
        "\n3. Change crouch to 'CTRL' and crouch-jump to 'SHIFT'? (yes/no)\nDefault: \"CTRL\" - crouch & \"SHIFT\" - crouch-jump\nUser Input: (yes / no)\nYour choice: ",
        lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
        "Unexpected input. Please enter 'yes' or 'no'."
    ).lower() in ['yes', 'y']
    
    print("=" * 70)
    disable_cartoon = get_valid_input(
        "\n4. Disable the original cartoony look?\nDefault: \"NO\" - enabled\nUser Input: (yes / no)\nYour choice: ",
        lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
        "Unexpected input. Please enter 'yes' or 'no'."
    ).lower() in ['yes', 'y']
    
    print("=" * 70)
    bind_left_bracket = input("\n5. Enter text to bind to '[' key:\nYour input: ")
    
    print("=" * 70)
    bind_right_bracket = input("\n6. Enter text to bind to ']' key:\nYour input: ")
    
    print("=" * 70)
    
    # Apply changes to lines
    changes = {
        'fps_max': lambda x: x.split()[0] + f" {fps_limit}\n",
        'bind ins': f'bind {ptt_key} "+voicerecord"',
        '// (press) \'ins\' starts voice recording': f"    // (press) '{ptt_key}' starts voice recording",
        'bind [': f'bind [ "say {bind_left_bracket}"',
        'bind ]': f'bind ] "say {bind_right_bracket}"'
    }

    if swap_crouch:
        changes.update({
            'bind shift "+duck"': 'bind ctrl "+duck"',
            'bind ctrl "+crouchJump"': 'bind shift "+crouchJump"',
            '// (press) \'shift\' crouches': "    // (press) 'ctrl' crouches",
            '// (press) \'ctrl\' jump-crouches': "    // (press) 'shift' jump-crouches"
        })

    if disable_cartoon:
        cartoon_settings = ['mat_phong', 'mat_specular', 'r_rimlight', 'mat_bumpmap']
        changes.update({setting: lambda x: x.replace("0", "1") if "0" in x else x.replace("1", "0") for setting in cartoon_settings})

    for i, line in enumerate(lines):
        for key, value in changes.items():
            if key in line:
                lines[i] = value(line) if callable(value) else f"{value}\n"
                break
    
    with autoexec_path.open('w', encoding='utf-8', errors='ignore') as file:
        file.writelines(lines)
    
    print("\nChanges have been made to the autoexec.cfg file.")

def prompt_for_changes(destination_folder):
    print("=" * 70)
    print(" " * 20 + "EXTRACTION SUCCESSFUL")
    print("=" * 70 + "\n")
    make_changes = get_valid_input(
        "Would you like to make any changes to the .cfg scripts? (yes/no): ",
        lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
        "Unexpected input. Please enter 'yes' or 'no'."
    ).lower() in ['yes', 'y']
    if make_changes:
        update_autoexec_cfg(destination_folder)
    else:
        print("\nNo changes will be made to the .cfg scripts.")
    
def main():
    display_startup_screen()
    
    try:
        tf2_cfg_path = find_tf2_install_directory()
        
        use_mastercomfig = get_valid_input(
            "Do you use Mastercomfig? (yes/no): ",
            lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
            "Unexpected input. Please enter 'yes' or 'no'."
        ).lower() in ['yes', 'y']
        destination_folder = tf2_cfg_path / "overrides" if use_mastercomfig else tf2_cfg_path
        
        with download_latest_release(LATEST_RELEASE_URL) as zip_file:
            destination_folder.mkdir(parents=True, exist_ok=True)
            extract_cfg_files(zip_file, destination_folder)
        
        prompt_for_changes(destination_folder)
        
        print("=" * 70)
        print(" " * 22 + "INSTALLATION SUCCESSFUL!")
        print("=" * 70)
        print(f"\nThe TF2 Masterclass Config has been successfully installed to:\n\"{destination_folder}\".")
        print("\nThank you for choosing to use my scripts!\n")
        print("=" * 70)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Detailed error information:")
        print(traceback.format_exc())  # This will print the full traceback

    finally:
        input("Press Enter to exit...")  # This ensures the console stays open

if __name__ == "__main__":
    main()