import os

# Path to your receptor.pdbqt
receptor_pdbqt = "model_01_new.pdbqt"

# Folder containing all ligand PDBQT files
ligand_folder = "output"

# Output folder where final PDBs will be stored
output_folder = "complex_pdbs"


# Make output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load receptor ATOM/HETATM lines
with open(receptor_pdbqt, 'r') as f:
    receptor_lines = [line for line in f if line.startswith("ATOM") or line.startswith("HETATM")]

# Loop over all ligands
for ligand_file in os.listdir(ligand_folder):
    if ligand_file.endswith(".pdbqt"):
        ligand_path = os.path.join(ligand_folder, ligand_file)
        
        ligand_lines = []
        with open(ligand_path, 'r') as f:
            in_model = False
            for line in f:
                if line.startswith("MODEL"):
                    in_model = True
                elif line.startswith("ENDMDL"):
                    break
                elif in_model:
                    ligand_lines.append(line)

        # Combine receptor and ligand
        merged_lines = receptor_lines + ligand_lines

        # Save as merged pdbqt
        output_file = ligand_file.replace(".pdbqt", "_complex.pdbqt")
        output_path = os.path.join(output_folder, output_file)
        with open(output_path, 'w') as out_f:
            out_f.writelines(merged_lines)
            out_f.write("END\n")

print(f"✅ Merged PDBQT complexes saved to: {output_folder}")
