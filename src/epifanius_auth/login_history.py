#riwayat login user
'''contoh: "Budi login pada 18 mei 2026
1.file handling
2.append mode
3.logging sederhana"'''
from datetime import datetime

def simpan_history(username, status="BERHASIL"):
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open("riwayat_login", "a") as file:
        file.write(f"[{waktu}] {username}:{status}\n")# ============================================================
# LOGIN HISTORY — Mencatat riwayat login ke file
# Struktur: [DD-MM-YYYY HH:MM:SS] username : STATUS
# Fitur:
#   1. File handling (append mode)
#   2. Timestamp otomatis dengan datetime
#   3. Logging sederhana (BERHASIL / GAGAL)
# ============================================================

import os
from datetime import datetime

HISTORY_FILE = "data/riwayat_login.txt"


def simpan_history(username: str, status: str = "BERHASIL"):
    """
    Menyimpan riwayat percobaan login ke file.

    Args:
        username : nama user yang mencoba login
        status   : 'BERHASIL' atau 'GAGAL' (default: 'BERHASIL')
    """
    os.makedirs("data", exist_ok=True)

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
        print("[!] Belum ada riwayat login.")
        return

    with open(HISTORY_FILE, "r") as f:
        baris_list = [b.strip() for b in f if b.strip()]

    if username:
        baris_list = [b for b in baris_list if f"] {username} :" in b]

    if not baris_list:
        print("[!] Tidak ada riwayat login yang ditemukan.")
        return

    print("\n╔══════════════════════════════════════════╗")
    print("║           RIWAYAT LOGIN                  ║")
    print("╚══════════════════════════════════════════╝")
    for baris in baris_list:
        print(f"  {baris}")
    print(f"\n  Total: {len(baris_list)} catatan")
