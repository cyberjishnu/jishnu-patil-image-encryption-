import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os, io, base64
from cryptography.fernet import Fernet

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("600x550")
app.title("🛡️ AES Image Encryption Tool")

selected_path = None
key_used = None

# Generate secure key
def generate_key():
    global key_used
    key_used = Fernet.generate_key()
    key_box.configure(state="normal")
    key_box.delete(0, ctk.END)
    key_box.insert(0, key_used.decode())
    key_box.configure(state="readonly")

# Choose image file
def choose_file():
    global selected_path
    selected_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if selected_path:
        img = Image.open(selected_path).resize((240, 240))
        img = ctk.CTkImage(img, size=(240, 240))
        image_preview.configure(image=img, text="")
        status_label.configure(text="Image selected ✔️", text_color="green")

# Encrypt image with AES
def encrypt_image():
    global key_used
    if not selected_path:
        status_label.configure(text="⚠️ No image selected!", text_color="red")
        return
    if not key_used:
        status_label.configure(text="⚠️ Generate or paste a key first!", text_color="red")
        return
    try:
        with open(selected_path, "rb") as img_file:
            img_bytes = img_file.read()
            f = Fernet(key_used)
            encrypted = f.encrypt(img_bytes)

            save_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted Files", "*.enc")])
            if save_path:
                with open(save_path, "wb") as out_file:
                    out_file.write(encrypted)
                status_label.configure(text="✅ Image Encrypted & Saved", text_color="green")
    except Exception as e:
        status_label.configure(text=str(e), text_color="red")

# Decrypt image with AES
def decrypt_image():
    global key_used
    if not key_used:
        status_label.configure(text="⚠️ Enter valid key to decrypt!", text_color="red")
        return
    path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    if not path:
        return
    try:
        with open(path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
            f = Fernet(key_used)
            decrypted = f.decrypt(encrypted_data)

            img = Image.open(io.BytesIO(decrypted))
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Images", "*.png")])
            if save_path:
                img.save(save_path)
                status_label.configure(text="✅ Image Decrypted & Saved", text_color="green")
    except Exception as e:
        status_label.configure(text="❌ " + str(e), text_color="red")

# GUI Layout
title = ctk.CTkLabel(app, text="🔐 AES Image Encryptor", font=("Segoe UI", 22, "bold"))
title.pack(pady=15)

btn_select = ctk.CTkButton(app, text="Choose Image", command=choose_file)
btn_select.pack()

image_preview = ctk.CTkLabel(app, text="(No Image Selected)", width=240, height=240)
image_preview.pack(pady=10)

key_label = ctk.CTkLabel(app, text="🔑 Encryption Key:")
key_label.pack()

key_box = ctk.CTkEntry(app, width=400)
key_box.pack()

generate_btn = ctk.CTkButton(app, text="Generate Key", command=generate_key)
generate_btn.pack(pady=10)

btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

encrypt_btn = ctk.CTkButton(btn_frame, text="Encrypt", command=encrypt_image, width=150)
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = ctk.CTkButton(btn_frame, text="Decrypt", command=decrypt_image, width=150)
decrypt_btn.grid(row=0, column=1, padx=10)

status_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 11))
status_label.pack(pady=10)

footer = ctk.CTkLabel(app, text="⚠️ Save your encryption key safely! Without it, the image can't be recovered.", font=("Segoe UI", 9), text_color="gray")
footer.pack(pady=5)

app.mainloop()
