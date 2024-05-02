import json
import random
import string
from cryptography.fernet import Fernet
import os

KEY_FILE = "key.txt"
PASSWORD_FILE = "passwords.txt"

def load_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        print("Hata: Anahtar dosyası bulunamadı.")
        print("Lütfen bir anahtar oluşturun.")
        exit()

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            data = file.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        with open(file_path + ".encrypted", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
    except FileNotFoundError:
        print(f"Hata: {file_path} dosyası bulunamadı.")

def decrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_path.replace(".encrypted", ""), "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
    except FileNotFoundError:
        print(f"Hata: {file_path} dosyası bulunamadı.")
    except Exception as e:
        print("Bir hata oluştu:", e)

def check_key_file():
    return os.path.exists(KEY_FILE)

def check_password_file():
    return os.path.exists(PASSWORD_FILE)

def remove_unencrypted_password_file():
    try:
        os.remove(PASSWORD_FILE)
        print("Şifrelenmemiş parola dosyası başarıyla silindi.")
    except FileNotFoundError:
        print("Şifrelenmemiş parola dosyası bulunamadı.")

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_password(site, password):
    try:
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    data[site] = password
    
    with open(PASSWORD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_password(site):
    try:
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
            return data.get(site, "Bu site için kaydedilmiş şifre bulunamadı.")
    except FileNotFoundError:
        return "Şifreleriniz kaydedilmemiş."

def delete_password(site):
    try:
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
            if site in data:
                del data[site]
                with open(PASSWORD_FILE, "w") as file:
                    json.dump(data, file, indent=4)
                print(f"{site} için kaydedilmiş şifre başarıyla silindi.")
            else:
                print(f"{site} için kaydedilmiş şifre bulunamadı.")
    except FileNotFoundError:
        print("Şifreleriniz kaydedilmemiş.")

def update_password(site, new_password):
    try:
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
            if site in data:
                data[site] = new_password
                with open(PASSWORD_FILE, "w") as file:
                    json.dump(data, file, indent=4)
                print(f"{site} için şifre başarıyla güncellendi.")
            else:
                print(f"{site} için kaydedilmiş şifre bulunamadı.")
    except FileNotFoundError:
        print("Şifreleriniz kaydedilmemiş.")

def main():
    if not check_key_file():
        generate_key()
    if not check_password_file():
        if os.path.exists(PASSWORD_FILE + ".encrypted"):
            key = load_key()
            decrypt_file(PASSWORD_FILE + ".encrypted", key)
            os.remove(PASSWORD_FILE + ".encrypted")
        else:
            print("Şifrelenmiş parola dosyası bulunamadı.")
            exit()

    while True:
        print("\nŞifre Yöneticisine Hoş Geldiniz!")
        print("1. Yeni şifre oluştur")
        print("2. Kaydedilmiş bir şifreyi getir")
        print("3. Bir şifreyi sil")
        print("4. Bir şifreyi güncelle")
        print("5. Çıkış")

        choice = input("Yapmak istediğiniz işlemi seçin: ").strip()

        if choice == "1":
            site = input("Şifre oluşturmak istediğiniz site/adresi girin: ")
            length = int(input("Şifrenizin uzunluğunu belirtin (varsayılan: 12): "))
            password = generate_password(length)
            save_password(site, password)
            print("Oluşturulan Şifre:", password)
            print(f"{site} için şifreniz başarıyla kaydedildi.")
        elif choice == "2":
            site = input("Şifresini görmek istediğiniz site/adresi girin: ")
            password = get_password(site)
            print(password)
        elif choice == "3":
            site = input("Silmek istediğiniz şifrenin site/adresini girin: ")
            delete_password(site)
        elif choice == "4":
            site = input("Güncellemek istediğiniz şifrenin site/adresini girin: ")
            new_password = input("Yeni şifreyi girin: ")
            update_password(site, new_password)
        elif choice == "5":
            key = load_key()
            encrypt_file(PASSWORD_FILE, key)
            remove_unencrypted_password_file()
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçenek. Lütfen 1 ile 5 arasında bir numara girin.")

if __name__ == "__main__":
    main()
