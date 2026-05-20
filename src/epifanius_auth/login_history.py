#riwayat login user
'''contoh: "Budi login pada 18 mei 2026
1.file handling
2.append mode
3.logging sederhana"'''
from datetime import datetime

def simpan_history(username, status="BERHASIL"):
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open("riwayat_login", "a") as file:
        file.write(f"[{waktu}] {username}:{status}\n")