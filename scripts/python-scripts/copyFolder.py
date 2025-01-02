import os
import shutil

def copy_folder_with_renaming(src_folder, dest_folder):
    """
    Copies the entire folder structure from src_folder to dest_folder.
    Appends '_copy' to the end of each file's name while copying, and skips subdirectories named 'labels'.

    Args:
        src_folder (str): Path to the source folder.
        dest_folder (str): Path to the destination folder.
    """
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return

    for root, dirs, files in os.walk(src_folder):
        # Skip subdirectories named 'labels'
        dirs[:] = [d for d in dirs if d != "labels"]

        # Create the corresponding destination folder structure
        relative_path = os.path.relpath(root, src_folder)
        dest_path = os.path.join(dest_folder, relative_path)
        os.makedirs(dest_path, exist_ok=True)

        # Copy and rename each file
        for file in files:
            src_file = os.path.join(root, file)
            # Add '_copy' before the file extension
            file_name, file_ext = os.path.splitext(file)
            dest_file = os.path.join(dest_path, f"{file_name}_copy{file_ext}")
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} -> {dest_file}")

    print(f"Folder '{src_folder}' copied to '{dest_folder}' with renamed files, excluding 'labels' directories.")

# Example usage
src_folder = "../../../../../../../Google Drive/My Drive/Datasets/final_fortnite_yolov8_dataset"  # Replace with the source folder path
dest_folder = "../../../../../../../Desktop/final_fortnite_color_yolov8_dataset"  # Replace with the destination folder path

copy_folder_with_renaming(src_folder, dest_folder)
