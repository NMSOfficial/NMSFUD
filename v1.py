import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

class Encoder:
    def __init__(self, root):
        self.root = root
        self.root.title("NMSFUD")
        self.root.geometry("500x300")
        self.root.config(bg="#2c3e50")

        self.dosya_yolu = None
        self.tur_sayisi_var = tk.IntVar()

        # Başlık ekle
        self.baslik_label = tk.Label(
            self.root, text="Multi-Algoritmalı Encoder", font=("Helvetica", 24, "bold"), fg="#ecf0f1", bg="#2c3e50"
        )
        self.baslik_label.pack(pady=10)

        # Şifreleme tur sayısı giriş alanı
        self.tur_sayisi_giris = ttk.Entry(self.root, textvariable=self.tur_sayisi_var, font=("Helvetica", 14))
        self.tur_sayisi_giris.pack(pady=10)
        self.tur_sayisi_giris.insert(0, "Şifreleme Tur Sayısı")

        # Dosya seçme butonu
        self.dosya_sec_buton = tk.Button(
            self.root, text="Dosya Seç", font=("Helvetica", 14), command=self.dosya_sec, bg="#2980b9", fg="#ecf0f1"
        )
        self.dosya_sec_buton.pack(pady=10)

        # Encode butonu
        self.encode_buton = tk.Button(
            self.root, text="Encode", font=("Helvetica", 14), command=self.encode, bg="#27ae60", fg="#ecf0f1"
        )
        self.encode_buton.pack(pady=10)

        # Çıkış butonu
        self.cikis_buton = tk.Button(
            self.root, text="Çıkış", font=("Helvetica", 14), command=self.root.quit, bg="#c0392b", fg="#ecf0f1"
        )
        self.cikis_buton.pack(pady=10)

    def dosya_sec(self):
        self.dosya_yolu = filedialog.askopenfilename(title="Dosya Seç", filetypes=(("Tüm Dosyalar", "*.*"),))
        if self.dosya_yolu:
            messagebox.showinfo("Dosya Seçildi", f"Seçilen Dosya: {self.dosya_yolu}")

    def encode(self):
        if not self.dosya_yolu:
            messagebox.showerror("Hata", "Lütfen bir dosya seçin")
            return

        tur_sayisi = self.tur_sayisi_var.get()
        if tur_sayisi <= 0:
            messagebox.showerror("Hata", "Lütfen geçerli bir şifreleme tur sayısı girin")
            return

        with open(self.dosya_yolu, 'rb') as dosya:
            veri = dosya.read()

        for i in range(tur_sayisi):
            veri = self.sifrele(veri)

        # Encode edilmiş dosyayı kaydet
        dosya_adi = os.path.basename(self.dosya_yolu)
        encoded_dosya_adi = os.path.splitext(dosya_adi)[0] + "_encoded" + os.path.splitext(dosya_adi)[1]
        encoded_file_path = os.path.join(os.path.dirname(self.dosya_yolu), encoded_dosya_adi)

        with open(encoded_file_path, 'wb') as dosya:
            dosya.write(veri)

        messagebox.showinfo("Başarılı", f"Dosya başarıyla {tur_sayisi} kez şifrelendi ve '{encoded_file_path}' olarak kaydedildi")

    def sifrele(self, veri):
        key = os.urandom(32)  # 256-bit anahtar
        iv = os.urandom(16)  # 128-bit IV

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(veri) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_data)  # IV ve şifrelenmiş veriyi birleştir ve base64 ile kodla

if __name__ == "__main__":
    root = tk.Tk()
    app = Encoder(root)
    root.mainloop()

