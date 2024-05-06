import tkinter as tk
from tkinter import filedialog, messagebox
import dragoncrypt

def select_file(entry_field):
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    entry_field.delete(0, tk.END)  # Clear the field first
    entry_field.insert(0, file_path)  # Insert the file path


def encrypt_file():
    keyword = password_entry.get()
    file_path = file_path_entry.get()

    if not file_path:  # Check if the file path entry is empty.
        messagebox.showwarning("Warning", "Please select a file to encrypt.")
        return

    if not keyword:
        messagebox.showwarning("Warning", "Please enter a password (keyword).")
        return
    
    # Check if the file already has the .drgenc extension
    if file_path.lower().endswith('.molten'):
        messagebox.showwarning("Error", "The selected file is already encrypted.")
        return

    # Proceed with encryption as the file is not already encrypted
    output_file_path = file_path + '.moltenc'
    
    try:
        dragoncrypt.encrypt_file(file_path, output_file_path, keyword)
        messagebox.showinfo("Success", f"File encrypted successfully as '{output_file_path}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_file():
    keyword = password_entry.get()
    file_path = file_path_entry.get()

    if not file_path:  # Check if the file path entry is empty.
        messagebox.showwarning("Warning", "Please select a file to decrypt.")
        return

    if not keyword:
        messagebox.showwarning("Warning", "Please enter a password (keyword).")
        return
    
    # Check if the file has the .drgenc extension and remove only that extension
    if file_path.lower().endswith('.moltenc'):
        output_file_path = file_path[:-len('.moltenc')]
    else:
        messagebox.showwarning("Warning", "The selected file does not have the .drgenc extension")
        return
    
    try:
        dragoncrypt.decrypt_file(file_path, output_file_path, keyword)
        messagebox.showinfo("Success", f"File decrypted successfully as '{output_file_path}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title('DragonCrypt')
root.geometry('400x350')  # Adjusted size as we have fewer widgets

# rest of the code to create the UI widgets
# ...

# Remove the output path label and entry creation
# Remove the select_output_button creation

# Adjust the position of the buttons since there are fewer widgets now
# ...


# Use 'bg' property to match the canvas color or use 'systemTransparent' for transparency
transparent_color = 'black'

# Use a canvas to add a background image
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(fill="both", expand=True)
# Load an image file you have for the texture
bg_image = tk.PhotoImage(file="/home/killswitch/dragoncrypt/dragonscrypt.png")
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Use Entries to show the selected file path
file_path_label = tk.Label(root, text="File to encrypt/decrypt:", bg=transparent_color, fg='white')
canvas.create_window(200, 50, window=file_path_label)

file_path_entry = tk.Entry(root)
canvas.create_window(200, 70, window=file_path_entry)

select_file_button = tk.Button(root, text="Select File", command=lambda: select_file(file_path_entry))
canvas.create_window(200, 95, window=select_file_button)

# Password Section
password_label = tk.Label(root, text="Password:", bg=transparent_color, fg='white')
canvas.create_window(200, 200, window=password_label)

password_entry = tk.Entry(root, show="*")
canvas.create_window(200, 220, window=password_entry)

# Buttons Section
encrypt_button = tk.Button(root, text='Encrypt File', command=encrypt_file)
canvas.create_window(125, 260, window=encrypt_button)

decrypt_button = tk.Button(root, text='Decrypt File', command=decrypt_file)
canvas.create_window(275, 260, window=decrypt_button)

quit_button = tk.Button(root, text='Quit', command=root.destroy)
canvas.create_window(200, 290, window=quit_button)

root.mainloop()
