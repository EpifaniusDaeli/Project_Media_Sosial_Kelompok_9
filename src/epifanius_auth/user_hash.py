# ============================================================
# PROJECT KELOMPOK: SOSIAL MEDIA CLI - STRUKTUR DATA HASH TABLE
# Metode Penanganan Collision: Separate Chaining
# ============================================================

class HashTable:
    # Inisialisasi awal tabel kosong
    def __init__(self, ukuran=16):
        self.ukuran = ukuran
        # Membuat list di dalam list (bucket) sebanyak ukuran tabel
        self.buckets = []
        for _ in range(ukuran):
            self.buckets.append([])
        self.jumlah_data = 0

    # ── Fungsi Hash (Menghitung Indeks) ──
    def hitung_hash(self, key):
        # Jumlahkan nilai ASCII dari semua karakter teks, lalu di-mod ukuran tabel
        total_ascii = 0
        for c in key.lower():
            total_ascii += ord(c)
        return total_ascii % self.ukuran

    # ── Fungsi Insert (Memasukkan Data Baru) ──
    def insert(self, key, value=""):
        idx = self.hitung_hash(key)
        bucket = self.buckets[idx]

        # Kalau key sudah ada di bucket, update nilainya (biar tidak duplikat)
        for i in range(len(bucket)):
            k, v = bucket[i]
            if k.lower() == key.lower():
                bucket[i] = (key, value)
                return

        # Kalau belum ada, tambahkan tuple baru ke dalam list bucket (Chaining)
        bucket.append((key, value))
        self.jumlah_data += 1

    # ── Fungsi Search (Mencari Data) ──
    def search(self, key):
        idx = self.hitung_hash(key)
        bucket = self.buckets[idx]

        # Cari data di dalam list bucket tertentu
        for k, v in bucket:
            if k.lower() == key.lower():
                return v # Kembalikan nilainya kalau ketemu
        return None

    # Fungsi pembantu untuk cek apakah data ada atau tidak (mengembalikan True/False)
    def exists(self, key):
        if self.search(key) is not None:
            return True
        return False

    # ── Fungsi Delete (Menghapus Data) ──
    def delete(self, key):
        idx = self.hitung_hash(key)
        bucket = self.buckets[idx]

        # Cari data berdasarkan indeks di dalam bucket lalu hapus
        for i in range(len(bucket)):
            k, v = bucket[i]
            if k.lower() == key.lower():
                bucket.pop(i)
                self.jumlah_data -= 1
                return True
        return False

    # ── Fungsi Cetak Tabel (Sangat Berguna Pas Demo Depan Dosen) ──
    def tampilkan(self):
        print("\n╔══════════════════════════════════════════╗")
        print("║          ISI HASH TABLE USER             ║")
        print("╚══════════════════════════════════════════╝")
        print(f"  Ukuran tabel : {self.ukuran} bucket")
        print(f"  Jumlah data  : {self.jumlah_data} user")
        print(f"  Fungsi hash  : sum(ASCII) mod {self.ukuran}")
        print("─" * 44)

        ada_isi = False
        for i in range(len(self.buckets)):
            bucket = self.buckets[i]
            if bucket:
                ada_isi = True
                # Gabungkan semua nama user di bucket yang sama
                isi_bucket = ""
                for k, v in bucket:
                    isi_bucket += k + ", "
                isi_bucket = isi_bucket.rstrip(", ")
                
                # Kasih tanda kalau terjadi collision (tabrakan)
                tag = ""
                if len(bucket) > 1:
                    tag = "  ← collision!"
                print(f"  [{i:>2}] {isi_bucket}{tag}")

        if not ada_isi:
            print("  (tabel kosong)")

    def count(self):
        return self.jumlah_data