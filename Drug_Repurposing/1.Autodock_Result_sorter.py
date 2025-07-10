import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        process_files()

def process_files():
    directory = folder_path.get()
    if not directory:
        messagebox.showerror("Error", "Please select a folder")
        return

    best_scores = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Check for text files
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
                start_reading = False
                for line in lines:
                    if start_reading and line.strip() and line.strip()[0].isdigit():
                        parts = line.strip().split()
                        if parts[0] == '1':  # We only want the best mode, which is the first mode
                            best_scores.append([filename] + parts[1:])
                            break
                    if 'mode |   affinity' in line:
                        start_reading = True

    if best_scores:
        df = pd.DataFrame(best_scores, columns=["File", "Affinity (kcal/mol)", "RMSD LB", "RMSD UB"])
        save_csv(df)
    else:
        messagebox.showinfo("Result", "No valid log files found.")

def save_csv(df):
    files = [('CSV Files', '*.csv')]
    file_path = filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title="Save file", initialfile="best_docking_scores.csv")
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"CSV file has been created at {file_path}")
    else:
        messagebox.showinfo("Cancelled", "Save operation cancelled")

def setup_gui():
    app = tk.Tk()
    app.title("AutoDock Vina Result Processor")

    global folder_path
    folder_path = tk.StringVar()

    browse_button = tk.Button(app, text="Browse Folder", command=browse_folder)
    browse_button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    setup_gui()
