import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

input_folder = "converted_pdbs"
output_base = "plip_output_fast"
os.makedirs(output_base, exist_ok=True)

pdb_files = [f for f in os.listdir(input_folder) if f.endswith(".pdb")]

# Function to run PLIP on one file
def run_plip(file):
    input_path = os.path.join(input_folder, file)
    ligand_name = file.replace(".pdb", "")
    output_path = os.path.join(output_base, ligand_name)
    os.makedirs(output_path, exist_ok=True)

    cmd = [
        "plip",
        "-f", input_path,
        "-o", output_path,
        "--name", ligand_name,
        "-t", "-x", "-y", "-v"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return file, result.returncode

# Parallel run with progress bar
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(run_plip, f) for f in pdb_files]
    for future in tqdm(as_completed(futures), total=len(futures), desc="🔬 PLIP Analysis Progress"):
        file, returncode = future.result()
        if returncode != 0:
            print(f"⚠️ Failed: {file}")
