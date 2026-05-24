# ============================================================
# NOTIF SLL — Sistem Notifikasi menggunakan Single Linked List
# Struktur data : Single Linked List (SLL)
# Setiap node hanya punya pointer ke node BERIKUTNYA (next)
# Fitur     :
#   1. Tambah notifikasi baru (di depan / head)
#   2. Tampilkan semua notifikasi
#   3. Hapus notifikasi terlama (dari tail)
#   4. Hitung total notifikasi
# ============================================================


class NotifNode:
    """Node dalam Single Linked List untuk satu notifikasi."""

    def __init__(self, pesan: str):
        self.pesan = pesan    # isi notifikasi
        self.next  = None     # pointer ke node berikutnya (SLL: hanya next, tidak ada prev)

    def __str__(self):
        return self.pesan


class NotifSLL:
    """
    Single Linked List untuk menyimpan antrian notifikasi.

    Struktur:
        head → [node1] → [node2] → [node3] → None
    Notifikasi terbaru ditambahkan di HEAD (depan).
    """

    def __init__(self):
        self.head = None   # node pertama (notifikasi terbaru)
        self._size = 0

    def tambah(self, pesan: str):
        """Menambahkan notifikasi baru di depan (O(1))."""
        node = NotifNode(pesan)
        node.next = self.head   # sambungkan ke list lama
        self.head = node        # jadikan head baru
        self._size += 1

    def tampilkan(self, username: str):
        """Menampilkan semua notifikasi milik user."""
        if self.is_empty():
            print("  (belum ada notifikasi)")
            return

        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║           NOTIFIKASI — @{username:<17}║")
        print(f"╚══════════════════════════════════════════╝")

        current = self.head
        nomor   = 1
        while current is not None:
            print(f"  {nomor}. {current.pesan}")
            current = current.next
            nomor  += 1

        print(f"\n  Total: {self._size} notifikasi")

    def hapus_terlama(self):
        """
        Menghapus notifikasi paling lama (tail / node terakhir).
        Perlu traversal O(n) karena SLL tidak punya pointer prev.
        """
        if self.is_empty():
            print("  [!] Tidak ada notifikasi untuk dihapus.")
            return

        # Jika hanya satu node
        if self.head.next is None:
            print(f"  [✓] Notifikasi dihapus: \"{self.head.pesan}\"")
            self.head  = None
            self._size = 0
            return

        # Traversal ke node sebelum tail
        current = self.head
        while current.next.next is not None:
            current = current.next

        print(f"  [✓] Notifikasi dihapus: \"{current.next.pesan}\"")
        current.next = None   # putuskan pointer ke tail
        self._size  -= 1

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self._size
