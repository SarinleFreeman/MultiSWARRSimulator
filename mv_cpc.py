import os
import glob
import shutil
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Copy specified files from a source directory to a destination directory.')
parser.add_argument('source_parent_dir', type=str,
                    help='Path to the parent directory containing the source directories.')
parser.add_argument('destination_parent_dir', type=str,
                    help='Path to the parent directory where the copied files will be saved.')
parser.add_argument('--files', nargs='+', help='List of file names to copy.', required=True)

# Parse command-line arguments
args = parser.parse_args()

# Main loop
source_parent_dir = os.path.join(os.getcwd(), args.source_parent_dir)
destination_parent_dir = os.path.join(os.getcwd(), args.destination_parent_dir)
files_to_copy = args.files

# Find all directories in the source_parent_dir
all_dirs = [d for d in glob.glob(os.path.join(source_parent_dir, '*')) if os.path.isdir(d)]

# Process each directory
for dir_path in all_dirs:
    # Create a new directory in the destination_parent_dir with the same name as the source directory
    dest_dir_path = os.path.join(destination_parent_dir, os.path.basename(dir_path))
    os.makedirs(dest_dir_path, exist_ok=True)

    # Copy the specified files from the source directory to the new directory
    for file_name in files_to_copy:
        src_file_path = os.path.join(dir_path, file_name)

        # Check if the file exists in the source directory
        if os.path.isfile(src_file_path):
            # Copy the file to the new directory
            shutil.copy2(src_file_path, os.path.join(dest_dir_path, file_name))
