import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import dragoncrypt
import os

def encrypt_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    keyword = simpledialog.askstring("Keyword", "Enter the encryption keyword:")
    if not keyword:
        messagebox.showwarning("Warning", "No keyword provided.")
        return

    output_file_path = filedialog.asksaveasfilename(defaultextension=".bin",
                                                    filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    if not output_file_path:
        return
    
    try:
        dragoncrypt.encrypt_file(file_path, output_file_path, keyword)
        messagebox.showinfo("Success", f"File encrypted successfully as '{output_file_path}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def decrypt_file():
    file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    if not file_path:
        return

    keyword = simpledialog.askstring("Keyword", "Enter the decryption keyword:")
    if not keyword:
        messagebox.showwarning("Warning", "No keyword provided.")
        return

    output_file_path = filedialog.asksaveasfilename(defaultextension="All files",
                                                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if not output_file_path:
        return
    
    try:
        dragoncrypt.decrypt_file(file_path, output_file_path, keyword)
        messagebox.showinfo("Success", f"File decrypted successfully as '{output_file_path}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title('DragonCrypt')

encrypt_button = tk.Button(root, text='Encrypt File', command=encrypt_file)
encrypt_button.pack()

decrypt_button = tk.Button(root, text='Decrypt File', command=decrypt_file)
decrypt_button.pack()

quit_button = tk.Button(root, text='Quit', command=root.destroy)
quit_button.pack()

root.mainloop()