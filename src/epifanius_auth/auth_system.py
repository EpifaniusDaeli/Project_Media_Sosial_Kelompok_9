# ============================================================
# PROJECT KELOMPOK: SOSIAL MEDIA CLI - MODUL AUTH
# Struktur data: List & Hash Table
# ============================================================

import os
from epifanius_auth.user_class import User
from epifanius_auth.login_history import simpan_history
from epifanius_auth.user_hash import HashTable

# Setup path file tempat menyimpan data akun user
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_FILE = os.path.join(_BASE_DIR, "data", "users.txt")


# Fungsi pembantu: ambil semua data user dari file users.txt
def baca_semua_user():
    users = []

    # Kalau file belum ada, langsung return list kosong
    if not os.path.exists(USERS_FILE):
        return users

    # Buka file dan baca baris per baris
    with open(USERS_FILE, "r") as f:
        for baris in f:
            baris = baris.strip()
            if not baris:
                continue
            data = baris.split(",", 1)
            if len(data) == 2:
                users.append(User(data[0], data[1]))

    return users


# Fungsi pembantu: mindahin data file ke hash table biar cepat dicek
def bangun_hash_table():
    users = baca_semua_user()
    
    # Inisialisasi ukuran hash table
    ukuran_tabel = 16
    if len(users) * 2 > 16:
        ukuran_tabel = len(users) * 2
        
    tabel = HashTable(ukuran=ukuran_tabel)
    
    # Masukkan semua username dan password ke hash table
    for u in users:
        tabel.insert(u.username, u.password)
    return tabel


# Fungsi untuk Menu Register Akun Baru
def register():
    print("\n╔══════════════════════════════════════════╗")
    print("║                REGISTER                  ║")
    print("╚══════════════════════════════════════════╝")

    # Siapkan hash table untuk cek duplikat username
    tabel = bangun_hash_table()

    # Loop input username sampai valid
    while True:
        username = input("  Username          : ").strip()

        if not username:
            print("  [!] Username tidak boleh kosong.")
            continue

        # Cek ke hash table apakah username sudah terpakai
        if tabel.exists(username):
            print(f"  [!] Username '{username}' sudah digunakan. Coba yang lain.")
            continue

        break # Keluar loop kalau username aman

    # Loop input password sampai valid
    while True:
        password = input("  Password           : ").strip()

        if len(password) < 4:
            print("  [!] Password minimal 4 karakter.")
            continue

        konfirmasi = input("  Konfirmasi password: ").strip()

        if password != konfirmasi:
            print("  [!] Password tidak cocok. Coba lagi.")
            continue

        break # Keluar loop kalau password cocok

    # Simpan akun baru ke file txt
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")

    print(f"\n  [✓] Akun '{username}' berhasil dibuat! Silakan login.")
    return True


# Fungsi untuk Menu Login
def login():
    print("\n╔══════════════════════════════════════════╗")
    print("║                 LOGIN                    ║")
    print("╚══════════════════════════════════════════╝")

    username = input("  Username : ").strip()
    password = input("  Password : ").strip()

    # Ambil data terbaru dari hash table untuk verifikasi login
    tabel = bangun_hash_table()

    # Proses pencarian di hash table (O(1))
    if tabel.exists(username):
        password_tersimpan = tabel.search(username)
        # Jika password di input sama dengan di hash table
        if password_tersimpan == password:
            simpan_history(username, "BERHASIL")
            print(f"\n  [✓] Login berhasil! Selamat datang, {username}.")
            return User(username, password)

    # Kalau username tidak ada atau password salah
    simpan_history(username, "GAGAL")
    print("\n  [✗] Username atau password salah.")
    return None