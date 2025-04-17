import os
import shutil
import re
import time

# the data is currently stuck within the 

source_dir = "dat/clean"
destination_root = "dat/data"

os.makedirs(destination_root,exist_ok = True)
moved_files = set()

while True:
    files = os.listdir(source_dir)

    for filename in files:
        if filename in moved_files:
            continue  # skip files already moved

        match = re.match(r"(\d+)_lr.*\.(hea|dat|png)", filename)
        if not match:
            continue

        number = int(match.group(1))
        folder_name = f"{(number // 1000):02d}000"
        dest_dir = os.path.join(destination_root, folder_name)
        os.makedirs(dest_dir, exist_ok=True)

        src_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_dir, filename)

        try:
            # Wait a short time in case the file is still being written
            # time.sleep(0.001)
            shutil.move(src_path, dest_path)
            moved_files.add(filename)
            print(f"Moved: {filename} → {folder_name}")
        except (PermissionError, FileNotFoundError) as e:
            print(f"Skipping {filename} (in use or not ready): {e}")
            continue
print("Files successfully reorganized")