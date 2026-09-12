import os
import shutil
import zipfile

base_dir = r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause"
zip_path = os.path.join(base_dir, "code.zip")
dest_dir = r"C:\Users\delig\OneDrive\Desktop\2026 Enactus\submission"
os.makedirs(dest_dir, exist_ok=True)

# Files to package into code.zip
files_to_zip = [
    ("main.py", "main.py"),
    ("solve.py", "solve.py"),
    ("solve_level1.py", "solve_level1.py"),
    ("solve_level2.py", "solve_level2.py"),
    ("solve_level3.py", "solve_level3.py"),
    ("solve_level4.py", "solve_level4.py"),
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

# Copy code.zip, solution.json, and level-specific solutions to desktop submission folder
dest_zip = os.path.join(dest_dir, "code.zip")
dest_sol = os.path.join(dest_dir, "solution.json")
dest_l1 = os.path.join(dest_dir, "level1_solution.json")
dest_l2 = os.path.join(dest_dir, "level2_solution.json")
dest_l3 = os.path.join(dest_dir, "level3_solution.json")
dest_l4 = os.path.join(dest_dir, "level4_solution.json")

shutil.copy2(zip_path, dest_zip)
shutil.copy2(os.path.join(base_dir, "solution.json"), dest_sol)
shutil.copy2(os.path.join(base_dir, "solutions", "level1_solution.json"), dest_l1)
shutil.copy2(os.path.join(base_dir, "solutions", "level2_solution.json"), dest_l2)
shutil.copy2(os.path.join(base_dir, "solutions", "level3_solution.json"), dest_l3)
shutil.copy2(os.path.join(base_dir, "solutions", "level4_solution.json"), dest_l4)

print(f"\nSuccessfully copied to {dest_dir}:")
print(f"  - code.zip ({os.path.getsize(dest_zip)} bytes)")
print(f"  - solution.json ({os.path.getsize(dest_sol)} bytes)")
print(f"  - level1_solution.json ({os.path.getsize(dest_l1)} bytes)")
print(f"  - level2_solution.json ({os.path.getsize(dest_l2)} bytes)")
print(f"  - level3_solution.json ({os.path.getsize(dest_l3)} bytes)")
print(f"  - level4_solution.json ({os.path.getsize(dest_l4)} bytes)")
