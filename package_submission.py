import os
import shutil
import zipfile

base_dir = r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause"
zip_path = os.path.join(base_dir, "code.zip")
dest_dir = r"C:\Users\delig\OneDrive\Desktop\2026 Enactus\submission"
os.makedirs(dest_dir, exist_ok=True)

# Files to package into code.zip
files_to_zip = [
    ("solve.py", "solve.py"),
    ("simulator.py", "simulator.py"),
    ("README.md", "README.md"),
]

# Add data folder
data_dir = os.path.join(base_dir, "data")
for fname in os.listdir(data_dir):
    fpath = os.path.join(data_dir, fname)
    if os.path.isfile(fpath):
        files_to_zip.append((os.path.join("data", fname), os.path.join("data", fname)))

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for rel_src, rel_dest in files_to_zip:
        full_src = os.path.join(base_dir, rel_src)
        zf.write(full_src, rel_dest)
        print(f"Added to zip: {rel_dest}")

print(f"Created {zip_path} (size: {os.path.getsize(zip_path)} bytes)")

# Copy code.zip and solution.json to desktop submission folder
dest_zip = os.path.join(dest_dir, "code.zip")
dest_sol = os.path.join(dest_dir, "solution.json")
shutil.copy2(zip_path, dest_zip)
shutil.copy2(os.path.join(base_dir, "solution.json"), dest_sol)

print(f"Successfully copied to {dest_dir}:")
print(f"  - code.zip ({os.path.getsize(dest_zip)} bytes)")
print(f"  - solution.json ({os.path.getsize(dest_sol)} bytes)")
