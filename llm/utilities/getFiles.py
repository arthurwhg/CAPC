import os
import glob


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
audioFolder = f"{ROOT_DIR}/data/tmp"
files = glob.glob(f"{audioFolder}/*.mp3")  # Get full paths
print(files)

# If only filenames are needed
files = [f for f in glob.glob(f"{audioFolder}/*") if os.path.isfile(f)]

print(files)