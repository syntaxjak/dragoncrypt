import tkinter as tk
from tkinter import filedialog, messagebox
import dragoncrypt

def encrypt_file():
    keyword = password_entry.get()
    if not keyword:
        messagebox.showwarning("Warning", "Please enter a password (keyword).")
        return
    
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if not file_path:
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
    keyword = password_entry.get()
    if not keyword:
        messagebox.showwarning("Warning", "Please enter a password (keyword).")
        return
    
    file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    if not file_path:
        return

    output_file_path = filedialog.asksaveasfilename(defaultextension=".png",
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

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")  # The show="*" ensures that the password is masked
password_entry.pack()

encrypt_button = tk.Button(root, text='Encrypt File', command=encrypt_file)
encrypt_button.pack()

decrypt_button = tk.Button(root, text='Decrypt File', command=decrypt_file)
decrypt_button.pack()

quit_button = tk.Button(root, text='Quit', command=root.destroy)
quit_button.pack()

root.mainloop()