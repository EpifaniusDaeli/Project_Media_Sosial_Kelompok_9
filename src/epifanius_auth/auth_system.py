# ============================================================
# AUTH SYSTEM — Sistem Autentikasi Pengguna
# Struktur data : List of User objects, Hash Table (cache cek username)
# Fitur     :
#   1. Register  : Tambah akun baru dengan validasi
#   2. Login     : Verifikasi username & password dari file
#   3. Hash Table digunakan untuk pengecekan username duplikat (O(1))
#   4. Simpan    : Data user ke data/users.txt (format: username,password)
# ============================================================

import os
from epifanius_auth.user_class  import User
from epifanius_auth.login_history import simpan_history
from epifanius_auth.user_hash   import HashTable

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


# ── Utilitas: bangun hash table dari semua username terdaftar ──
def _bangun_hash_table() -> HashTable:
    """
    Membangun HashTable dari seluruh username di file.
    Digunakan untuk pengecekan duplikat O(1) saat register.
    """
    users = _baca_semua_user()
    tabel = HashTable(ukuran=max(16, len(users) * 2))
    for u in users:
        tabel.insert(u.username, u.password)
    return tabel


# ── Register ──
def register() -> bool:
    """
    Mendaftarkan akun baru.

    Validasi:
      - Username tidak boleh kosong dan belum dipakai (cek via Hash Table)
      - Password minimal 4 karakter
      - Konfirmasi password harus cocok

    Returns:
        True jika registrasi berhasil, False jika dibatalkan.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║               REGISTER                   ║")
    print("╚══════════════════════════════════════════╝")

    # Bangun hash table sekali untuk semua pengecekan duplikat
    tabel = _bangun_hash_table()

    # ── Input & validasi username ──
    while True:
        username = input("  Username          : ").strip()

        if not username:
            print("  [!] Username tidak boleh kosong.")
            continue

        # Cek duplikat menggunakan Hash Table — O(1) rata-rata
        if tabel.exists(username):
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
      2. Cari kecocokan menggunakan Hash Table (O(1))
      3. Verifikasi password
      4. Catat riwayat login (BERHASIL / GAGAL)

    Returns:
        Objek User jika berhasil, None jika gagal.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║                 LOGIN                    ║")
    print("╚══════════════════════════════════════════╝")

    username = input("  Username : ").strip()
    password = input("  Password : ").strip()

    # Bangun hash table lalu cari username — O(1) rata-rata
    tabel = _bangun_hash_table()

    if tabel.exists(username):
        password_tersimpan = tabel.search(username)
        if password_tersimpan == password:
            simpan_history(username, "BERHASIL")
            print(f"\n  [✓] Login berhasil! Selamat datang, {username}.")
            return User(username, password)

    # Tidak ditemukan atau password salah
    simpan_history(username, "GAGAL")
    print("\n  [✗] Username atau password salah.")
    return None
