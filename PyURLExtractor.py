import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder():
    """Open a dialog to select a folder."""
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def select_save_file():
    """Open a dialog to select a save file location."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    save_entry.delete(0, tk.END)
    save_entry.insert(0, file_path)

def extract_urls():
    """Extract URLs based on the regex pattern and save to a file."""
    folder = folder_entry.get()
    pattern = pattern_entry.get()
    save_path = save_entry.get()

    if not folder or not pattern or not save_path:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path.")
        return

    urls = []
    try:
        regex = re.compile(pattern)
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            urls.extend(regex.findall(line))
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

        # Save the URLs to the specified file
        with open(save_path, "w", encoding="utf-8") as f:
            f.write("\n".join(urls))

        messagebox.showinfo("Success", f"Extracted {len(urls)} URLs to {save_path}")
    except re.error as e:
        messagebox.showerror("Regex Error", f"Invalid regex pattern: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter GUI setup
root = tk.Tk()
root.title("PyURLExtractor")

# Folder selection
tk.Label(root, text="Folder to search:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_folder).grid(row=0, column=2, padx=10, pady=5)

# Regex pattern
tk.Label(root, text="Regex pattern:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
pattern_entry = tk.Entry(root, width=50)
pattern_entry.insert(0, r"https?://[^\s]+")  # Default regex for URLs
pattern_entry.grid(row=1, column=1, padx=10, pady=5)

# Save file location
tk.Label(root, text="Save to file:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
save_entry = tk.Entry(root, width=50)
save_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_save_file).grid(row=2, column=2, padx=10, pady=5)

# Extract button
tk.Button(root, text="Extract URLs", command=extract_urls, bg="lightblue").grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
