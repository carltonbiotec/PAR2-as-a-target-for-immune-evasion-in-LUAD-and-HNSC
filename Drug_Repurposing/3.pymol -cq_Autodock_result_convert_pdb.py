import os

input_folder = "complex_pdbs"
output_folder = "converted_pdbs"
os.makedirs(output_folder, exist_ok=True)

files = [f for f in os.listdir(input_folder) if f.endswith(".pdbqt")]

for f in files:
    try:
        full_input = os.path.join(input_folder, f)
        name = f.replace(".pdbqt", "")
        cmd.load(full_input, name)
        output_path = os.path.join(output_folder, name + ".pdb")
        cmd.save(output_path, name)
        cmd.delete(name)
        print(f"✅ Converted {f} to PDB.")
    except Exception as e:
        print(f"❌ Failed to convert {f}: {e}")
