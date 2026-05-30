# ============================================================
# PROJECT KELOMPOK: SOSIAL MEDIA CLI - MODUL LOGIN HISTORY
# Struktur data: File Handling (Append & Read Mode)
# ============================================================

import os
from datetime import datetime

# Setup path folder dan file tempat menyimpan riwayat login
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY_FILE = os.path.join(_BASE_DIR, "data", "riwayat_login.txt")


# Fungsi untuk mencatat aktivitas login (sukses/gagal) ke file
def simpan_history(username, status="BERHASIL"):
    # Buat folder data secara otomatis jika belum ada
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    # Ambil waktu sekarang dan format menjadi Hari-Bulan-Tahun Jam:Menit:Detik
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Buka file riwayat dengan mode 'a' (Append) supaya nambah di baris bawah
    with open(HISTORY_FILE, "a") as f:
        f.write(f"[{waktu}] {username} : {status}\n")


# Fungsi untuk membaca dan menampilkan riwayat login di CLI
def tampilkan_history(username=None):
    # Cek dulu apakah file riwayatnya ada atau tidak
    if not os.path.exists(HISTORY_FILE):
        print("  [!] Belum ada riwayat login.")
        return

    # Baca file teks dan masukkan tiap barisnya ke dalam sebuah List
    with open(HISTORY_FILE, "r") as f:
        baris_list = []
        for b in f:
            if b.strip():  # Pastikan bukan baris kosong
                baris_list.append(b.strip())

    # Jika ada filter username, saring List agar hanya menampilkan user tersebut
    if username:
        baris_filtered = []
        for b in baris_list:
            if f"] {username} :" in b:
                baris_filtered.append(b)
        baris_list = baris_filtered

    # Jika setelah disaring ternyata kosong, tampilkan pesan kosong
    if not baris_list:
        print("  [!] Tidak ada riwayat login yang ditemukan.")
        return

    # Cetak hasil riwayat login ke layar CLI
    print("\n╔══════════════════════════════════════════╗")
    print("║            RIWAYAT LOGIN                 ║")
    print("╚══════════════════════════════════════════╝")
    for baris in baris_list:
        print(f"  {baris}")
    print(f"\n  Total: {len(baris_list)} catatan")