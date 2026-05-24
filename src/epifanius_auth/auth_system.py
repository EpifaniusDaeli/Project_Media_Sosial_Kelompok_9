# ============================================================
# AUTH SYSTEM — Sistem Autentikasi Pengguna
# Struktur data : List of User objects, File handling
# Fitur     :
#   1. Register  : Tambah akun baru dengan validasi
#   2. Login     : Verifikasi username & password dari file
#   3. Simpan    : Data user ke data/users.txt (format: username,password)
# ============================================================

import os
from epifanius_auth.user_class import User
from epifanius_auth.login_history import simpan_history

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_FILE = os.path.join(_BASE_DIR, "data", "users.txt")


# ── Utilitas: baca semua user dari file ──
def _baca_semua_user() -> list:
    """Membaca seluruh data user dari file dan mengembalikan list User."""
    users = []

    if not os.path.exists(USERS_FILE):
        return users

    with open(USERS_FILE, "r") as f:
        for baris in f:
            baris = baris.strip()
            if not baris:
                continue
            data = baris.split(",", 1)
            if len(data) == 2:
                users.append(User(data[0], data[1]))

    return users


# ── Utilitas: cek apakah username sudah terdaftar ──
def _username_tersedia(username: str) -> bool:
    """Mengembalikan True jika username belum dipakai."""
    users = _baca_semua_user()
    return all(u.username.lower() != username.lower() for u in users)


# ── Register ──
def register() -> bool:
    """
    Mendaftarkan akun baru.

    Validasi:
      - Username tidak boleh kosong dan belum dipakai
      - Password minimal 4 karakter
      - Konfirmasi password harus cocok

    Returns:
        True jika registrasi berhasil, False jika dibatalkan.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║               REGISTER                   ║")
    print("╚══════════════════════════════════════════╝")

    # ── Input & validasi username ──
    while True:
        username = input("  Username          : ").strip()

        if not username:
            print("  [!] Username tidak boleh kosong.")
            continue

        if not _username_tersedia(username):
            print(f"  [!] Username '{username}' sudah digunakan. Coba yang lain.")
            continue

        break   # username valid

    # ── Input & validasi password ──
    while True:
        password = input("  Password           : ").strip()

        if len(password) < 4:
            print("  [!] Password minimal 4 karakter.")
            continue

        konfirmasi = input("  Konfirmasi password: ").strip()

        if password != konfirmasi:
            print("  [!] Password tidak cocok. Coba lagi.")
            continue

        break   # password valid

    # ── Simpan ke file ──
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")

    print(f"\n  [✓] Akun '{username}' berhasil dibuat! Silakan login.")
    return True


# ── Login ──
def login():
    """
    Melakukan proses login.

    Proses:
      1. Input username & password
      2. Cari kecocokan di data/users.txt
      3. Catat riwayat login (BERHASIL / GAGAL)

    Returns:
        Objek User jika berhasil, None jika gagal.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║                 LOGIN                    ║")
    print("╚══════════════════════════════════════════╝")

    username = input("  Username : ").strip()
    password = input("  Password : ").strip()

    users = _baca_semua_user()

    for user in users:
        if user.username == username and user.cek_password(password):
            simpan_history(username, "BERHASIL")
            print(f"\n  [✓] Login berhasil! Selamat datang, {username}.")
            return user

    # Tidak ditemukan
    simpan_history(username, "GAGAL")
    print("\n  [✗] Username atau password salah.")
    return None
