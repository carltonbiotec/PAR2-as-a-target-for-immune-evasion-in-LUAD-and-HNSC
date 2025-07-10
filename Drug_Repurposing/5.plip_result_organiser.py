import os
import pandas as pd
from pathlib import Path

input_dir = "plip_output_fast"
interaction_data = {
    "Hydrophobic_Interactions": [],
    "Hydrogen_Bonds": [],
    "Pi_Stacking": []
}

for folder in os.listdir(input_dir):
    txt_path = os.path.join(input_dir, folder, f"{folder}.txt")
    if not os.path.exists(txt_path):
        continue
    complex_id = folder

    with open(txt_path, "r") as f:
        lines = f.readlines()

    current_block = None
    headers = []
    for line in lines:
        if line.strip().startswith("**") and line.strip().endswith("**"):
            block_name = line.strip().replace("**", "").replace(" ", "_")
            current_block = block_name
            headers = []
            continue

        if current_block and line.strip().startswith("|") and not headers:
            # This is the header row
            headers = [h.strip() for h in line.strip().strip("|").split("|")]
            continue

        if current_block and line.strip().startswith("|") and headers:
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) != len(headers):
                continue
            row = dict(zip(headers, parts))
            row["Complex"] = complex_id

            if current_block == "Hydrophobic_Interactions":
                interaction_data["Hydrophobic_Interactions"].append({
                    "Complex": complex_id,
                    "Residue": f"{row['RESTYPE']} {row['RESNR']} ({row['RESCHAIN']})",
                    "Ligand": f"{row['RESTYPE_LIG']} {row['RESNR_LIG']} ({row['RESCHAIN_LIG']})",
                    "Distance": float(row["DIST"])
                })

            elif current_block == "Hydrogen_Bonds":
                interaction_data["Hydrogen_Bonds"].append({
                    "Complex": complex_id,
                    "Residue": f"{row['RESTYPE']} {row['RESNR']} ({row['RESCHAIN']})",
                    "Ligand": f"{row['RESTYPE_LIG']} {row['RESNR_LIG']} ({row['RESCHAIN_LIG']})",
                    "Distance_D-A": float(row["DIST_D-A"]),
                    "Distance_H-A": float(row["DIST_H-A"]),
                    "Donor": "Protein" if row["PROTISDON"].lower() == "true" else "Ligand"
                })

            elif current_block == "pi-Stacking":
                interaction_data["Pi_Stacking"].append({
                    "Complex": complex_id,
                    "Residue": f"{row['RESTYPE']} {row['RESNR']} ({row['RESCHAIN']})",
                    "Ligand": f"{row['RESTYPE_LIG']} {row['RESNR_LIG']} ({row['RESCHAIN_LIG']})",
                    "Distance": float(row["CENTDIST"]),
                    "Angle": float(row["ANGLE"]),
                    "Type": "Parallel" if row["TYPE"] == "P" else "T-shaped"
                })

# Write to Excel
out_path = "PLIP_Interaction_Summary.xlsx"
with pd.ExcelWriter(out_path) as writer:
    for interaction, records in interaction_data.items():
        if records:
            df = pd.DataFrame(records)
            df.to_excel(writer, sheet_name=interaction, index=False)

print(f"✅ Saved interaction summary to: {out_path}")
