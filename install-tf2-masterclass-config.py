import os
import zipfile
from pathlib import Path
import platform
from io import BytesIO
from urllib.request import urlopen

GITHUB_REPO_URL = "https://github.com/7eventy7/TF2-MASTERCLASS-CONFIG"
LATEST_RELEASE_URL = f"{GITHUB_REPO_URL}/releases/latest/download/TF2-MASTERCLASS-CONFIG.zip"

LENNY_FACES = {
    "0": "( ͡ಠ ʖ̯ ͡ಠ)",  # sadge
    "1": "( ͝° ͜ʖ͡°)",  # skeptical
    "2": "( ͡° ͜ ͡°)",  # nose less
    "3": "( ͡o ͜ʖ ͡o)",  # wide eyed
    "4": "( ͠° ͟ʖ ͡°)",  # upset
    "5": "( ͡~ ͜ʖ ͡°)"   # wink
}

LENNY_NAMES = {
    "0": "sadge",
    "1": "skeptical",
    "2": "nose less",
    "3": "wide eyed",
    "4": "upset",
    "5": "wink"
}

def display_startup_screen():
    print("="*70)
    print(" " * 20 + "TF2 MASTERCLASS CONFIG INSTALLER")
    print("="*70)
    print(" " * 25 + "v2.1.3 -- June 18th, 2024")
    print("="*70)
    print("\nThis script will help you install the TF2 Masterclass Config.")
    print("Please follow the instructions as prompted.\n")
    print("="*70 + "\n")

def find_tf2_install_directory():
    possible_paths = []
    if platform.system() == "Windows":
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            path = Path(f"{drive}:\\")
            if path.exists():
                possible_paths.append(path / "Program Files (x86)" / "Steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg")
                possible_paths.append(path / "steam" / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg")
                for root, dirs, files in os.walk(path):
                    if "steamapps" in dirs:
                        steam_path = Path(root) / "steamapps" / "common" / "Team Fortress 2" / "tf" / "cfg"
                        possible_paths.append(steam_path)
                        break

    for path in possible_paths:
        if path.exists():
            print(f"TF2 install directory found:\n\"{path}\"\n")
            return path

    raise FileNotFoundError("TF2 install directory not found in any of the steamapps directories")

def download_latest_release(url):
    response = urlopen(url)
    if response.status != 200:
        raise Exception(f"Failed to download file: {response.reason}")
    print("Downloaded latest release from GitHub\n")
    return BytesIO(response.read())

def extract_cfg_files(zip_file, destination_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.cfg'):
                zip_ref.extract(file, destination_folder)
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
    print("="*70)
    fps_limit = get_valid_input(
        "\n1. What is your desired fps limit?\nDefault: \"0\" - Disabled\nUser Input: (0 thru 1000)\nYour choice: ",
        lambda x: x.isdigit() and 0 <= int(x) <= 1000,
        "Unexpected input. Please enter a number between 0 and 1000."
    ) or "0"
    
    print("="*70)
    ptt_key = input("\n2. Change the push to talk keybind?\nDefault: \"INS\" - Insert\nUser Input: (Any single keybind)\nYour choice: ").strip() or "ins"
    
    print("="*70)
    swap_crouch = get_valid_input(
        "\n3. Change crouch to 'CTRL' and crouch-jump to 'SHIFT'? (yes/no)\nDefault: \"CTRL\" - crouch & \"SHIFT\" - crouch-jump\nUser Input: (yes / no)\nYour choice: ",
        lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
        "Unexpected input. Please enter 'yes' or 'no'."
    ).lower() in ['yes', 'y']
    
    print("="*70)
    disable_cartoon = get_valid_input(
        "\n4. Disable the original cartoony look?\nDefault: \"NO\" - enabled\nUser Input: (yes / no)\nYour choice: ",
        lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
        "Unexpected input. Please enter 'yes' or 'no'."
    ).lower() in ['yes', 'y']
    
    print("="*70)
    for key, value in LENNY_NAMES.items():
        print(f"({key}) - {value}")
    lenny1 = get_valid_input(
        "\n5. Which first lenny shall be bound to '['?\nDefault: \"0\" - sadge\nUser Input: (0 thru 5)\nYour choice: ",
        lambda x: x in LENNY_FACES,
        "Unexpected input. Please enter a number between 0 and 5."
    ) or "0"
    
    print("="*70)
    for key, value in LENNY_NAMES.items():
        print(f"({key}) - {value}")
    lenny2 = get_valid_input(
        "\n6. Which second lenny shall be bound to ']'?\nDefault: \"1\" - skeptical\nUser Input: (0 thru 5)\nYour choice: ",
        lambda x: x in LENNY_FACES,
        "Unexpected input. Please enter a number between 0 and 5."
    ) or "1"
    
    print("="*70)
    
    # Apply changes to lines
    for i, line in enumerate(lines):
        if "fps_max" in line:
            lines[i] = f'fps_max {fps_limit}\n'
        if "bind ins" in line:
            lines[i] = f'bind {ptt_key} "+voicerecord"\n'
        if "// (press) 'ins' starts voice recording" in line:
            lines[i] = f"    // (press) '{ptt_key}' starts voice recording\n"
        if swap_crouch:
            if "bind shift" in line and "+duck" in line:
                lines[i] = 'bind ctrl "+duck"\n'
            if "bind ctrl" in line and "+crouchJump" in line:
                lines[i] = 'bind shift "+crouchJump"\n'
            if "// (press) 'shift' crouches" in line:
                lines[i] = "    // (press) 'ctrl' crouches\n"
            if "// (press) 'ctrl' jump-crouches" in line:
                lines[i] = "    // (press) 'shift' jump-crouches\n"
        if disable_cartoon:
            if "mat_phong" in line:
                lines[i] = line.replace("0", "1") if "0" in line else line.replace("1", "0")
            if "mat_specular" in line:
                lines[i] = line.replace("0", "1") if "0" in line else line.replace("1", "0")
            if "r_rimlight" in line:
                lines[i] = line.replace("0", "1") if "0" in line else line.replace("1", "0")
            if "mat_bumpmap" in line:
                lines[i] = line.replace("0", "1") if "0" in line else line.replace("1", "0")
        if "bind [" in line:
            lines[i] = f'bind [ "say {LENNY_FACES[lenny1]}"\n'
        if "bind ]" in line:
            lines[i] = f'bind ] "say {LENNY_FACES[lenny2]}"\n'
    
    with autoexec_path.open('w', encoding='utf-8', errors='ignore') as file:
        file.writelines(lines)
    
    print("\nChanges have been made to the autoexec.cfg file.")

def prompt_for_changes(destination_folder):
    print("="*70)
    print(" " * 20 + "EXTRACTION SUCCESSFUL")
    print("="*70 + "\n")
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
        
        # Ask the user if they use Mastercomfig
        use_mastercomfig = get_valid_input(
            "Do you use Mastercomfig? (yes/no): ",
            lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
            "Unexpected input. Please enter 'yes' or 'no'."
        ).lower() in ['yes', 'y']
        if use_mastercomfig:
            destination_folder = tf2_cfg_path / "overrides"
        else:
            destination_folder = tf2_cfg_path
        
        # Download the latest release from GitHub
        zip_file = download_latest_release(LATEST_RELEASE_URL)
        
        # Extract to the chosen destination folder
        destination_folder.mkdir(parents=True, exist_ok=True)
        extract_cfg_files(zip_file, destination_folder)
        
        # Delete the downloaded .zip file
        zip_file.close()
        
        # Prompt for changes to the .cfg scripts
        prompt_for_changes(destination_folder)
        
        # Display installation successful message
        print("="*70)
        print(" " * 22 + "INSTALLATION SUCCESSFUL!")
        print("="*70)
        print(f"\nThe TF2 Masterclass Config has been successfully installed to:\n\"{destination_folder}\".")
        print("\nThank you for choosing to use my scripts!\n")
        print("="*70)

        # Wait for user input before exiting
        input("Press any button to exit...")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
