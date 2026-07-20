from pathlib import Path

def get_files_from_folders(folder1_path, folder2_path):
    # Convert string paths to Path objects
    path1 = Path(folder1_path)
    path2 = Path(folder2_path)
    
    # Check if directories exist to avoid errors
    if not path1.is_dir() or not path2.is_dir():
        return "Error: One or both folder paths do not exist or are not directories."

    # Extract just the file names (ignoring sub-folders)
    folder1_files = [file.name for file in path1.iterdir() if file.is_file()]
    folder2_files = [file.name for file in path2.iterdir() if file.is_file()]
    
    # Combine the two lists
    combined_files = folder1_files + folder2_files
    
    return combined_files

# --- Example Usage ---
# Replace these with the actual paths on your computer
folder_a = r"G:\Math\Pcap Generator\data\raw_pcaps\NonVPN-PCAPs-02"
folder_b = r"G:\Math\Pcap Generator\data\raw_pcaps\NonVPN-PCAPs-01"

# Get the list and print it
all_filenames = get_files_from_folders(folder_a, folder_b)
print(all_filenames)