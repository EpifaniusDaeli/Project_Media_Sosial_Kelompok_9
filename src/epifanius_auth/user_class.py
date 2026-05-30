# ============================================================
# PROJECT KELOMPOK: SOSIAL MEDIA CLI - MODUL USER CLASS
# Konsep: Pemrograman Berorientasi Objek (OOP) - Encapsulation
# ============================================================

class User:
    # Constructor untuk inisialisasi objek user baru
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Method bawaan untuk mengubah objek menjadi string saat dicetak
    def __str__(self):
        return f"User(username='{self.username}')"

    # Method untuk mencocokkan input password dengan password asli
    def cek_password(self, password):
        return self.password == password