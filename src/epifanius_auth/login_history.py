# ============================================================
# LOGIN HISTORY — Mencatat riwayat login ke file
# Struktur  : [DD-MM-YYYY HH:MM:SS] username : STATUS
# Struktur data : File handling (append mode)
# Fitur     :
#   1. Timestamp otomatis dengan datetime
#   2. Logging sederhana (BERHASIL / GAGAL)
# ============================================================

import os
from datetime import datetime

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY_FILE = os.path.join(_BASE_DIR, "data", "riwayat_login.txt")


def simpan_history(username: str, status: str = "BERHASIL"):
    """
    Menyimpan riwayat percobaan login ke file.

    Args:
        username : nama user yang mencoba login
        status   : 'BERHASIL' atau 'GAGAL' (default: 'BERHASIL')
    """
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open(HISTORY_FILE, "a") as f:
        f.write(f"[{waktu}] {username} : {status}\n")


def tampilkan_history(username: str = None):
    """
    Menampilkan riwayat login dari file.
    Jika username diberikan, hanya tampilkan riwayat user tersebut.

    Args:
        username : filter berdasarkan user (opsional)
    """
    if not os.path.exists(HISTORY_FILE):
        print("  [!] Belum ada riwayat login.")
        return

    with open(HISTORY_FILE, "r") as f:
        baris_list = [b.strip() for b in f if b.strip()]

    if username:
        baris_list = [b for b in baris_list if f"] {username} :" in b]

    if not baris_list:
        print("  [!] Tidak ada riwayat login yang ditemukan.")
        return

    print("\n╔══════════════════════════════════════════╗")
    print("║           RIWAYAT LOGIN                  ║")
    print("╚══════════════════════════════════════════╝")
    for baris in baris_list:
        print(f"  {baris}")
    print(f"\n  Total: {len(baris_list)} catatan")
