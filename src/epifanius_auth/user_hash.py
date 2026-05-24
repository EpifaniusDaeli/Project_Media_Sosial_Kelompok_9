# ============================================================
# USER HASH TABLE — Hash Table manual untuk indeks username
# Struktur data : Hash Table dengan Separate Chaining
# Fungsi hash  : jumlah nilai ASCII karakter mod ukuran tabel
# Collision    : diselesaikan dengan chaining (list per bucket)
# Fitur     :
#   1. Insert username ke tabel
#   2. Search username (O(1) rata-rata)
#   3. Delete username dari tabel
#   4. Tampilkan isi tabel (untuk debugging / edukasi)
# ============================================================


class HashTable:
    """
    Hash Table dengan Separate Chaining.

    Setiap slot (bucket) menyimpan list pasangan (key, value).
    Collision ditangani dengan menambah ke list bucket yang sama.

    Contoh dengan ukuran 8:
        bucket[0]: []
        bucket[1]: [("budi", "data")]
        bucket[2]: [("andi", "data"), ("caca", "data")]  ← collision
        ...
    """

    def __init__(self, ukuran: int = 16):
        self.ukuran  = ukuran
        self.buckets = [[] for _ in range(ukuran)]   # list of lists
        self._count  = 0

    # ── Fungsi Hash ──
    def _hash(self, key: str) -> int:
        """
        Menghitung indeks bucket dari key (string).
        Algoritma: jumlah nilai ASCII semua karakter, mod ukuran tabel.

        Contoh: "budi" → (98+117+100+105) % 16 = 420 % 16 = 4
        """
        return sum(ord(c) for c in key.lower()) % self.ukuran

    # ── Insert ──
    def insert(self, key: str, value: str = ""):
        """
        Menyimpan pasangan key-value ke tabel.
        Jika key sudah ada, value diperbarui.
        """
        idx    = self._hash(key)
        bucket = self.buckets[idx]

        # Cek apakah key sudah ada di bucket ini (update)
        for i, (k, v) in enumerate(bucket):
            if k.lower() == key.lower():
                bucket[i] = (key, value)
                return

        # Belum ada → tambahkan (chaining)
        bucket.append((key, value))
        self._count += 1

    # ── Search ──
    def search(self, key: str) -> str | None:
        """
        Mencari value berdasarkan key.
        Kembalikan value jika ditemukan, None jika tidak.
        Rata-rata O(1), worst case O(n) jika semua hash bertabrakan.
        """
        idx    = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k.lower() == key.lower():
                return v

        return None   # tidak ditemukan

    def exists(self, key: str) -> bool:
        """Mengembalikan True jika key ada di tabel."""
        return self.search(key) is not None

    # ── Delete ──
    def delete(self, key: str) -> bool:
        """
        Menghapus key dari tabel.
        Kembalikan True jika berhasil, False jika key tidak ditemukan.
        """
        idx    = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k.lower() == key.lower():
                bucket.pop(i)
                self._count -= 1
                return True

        return False

    # ── Build dari list ──
    @classmethod
    def dari_list(cls, usernames: list) -> "HashTable":
        """
        Membuat HashTable baru dari daftar username.
        Dipakai untuk membangun cache cepat saat program mulai.
        """
        tabel = cls(ukuran=max(16, len(usernames) * 2))
        for u in usernames:
            tabel.insert(u, u)
        return tabel

    # ── Tampilkan isi tabel (untuk edukasi) ──
    def tampilkan(self):
        """Menampilkan isi setiap bucket — berguna untuk presentasi."""
        print("\n╔══════════════════════════════════════════╗")
        print("║          ISI HASH TABLE USER             ║")
        print("╚══════════════════════════════════════════╝")
        print(f"  Ukuran tabel : {self.ukuran} bucket")
        print(f"  Jumlah data  : {self._count} user")
        print(f"  Fungsi hash  : sum(ASCII) mod {self.ukuran}")
        print("─" * 44)

        ada_isi = False
        for i, bucket in enumerate(self.buckets):
            if bucket:
                ada_isi = True
                keys = ", ".join(k for k, v in bucket)
                tag  = "  ← collision!" if len(bucket) > 1 else ""
                print(f"  [{i:>2}] {keys}{tag}")

        if not ada_isi:
            print("  (tabel kosong)")

    def count(self) -> int:
        return self._count
