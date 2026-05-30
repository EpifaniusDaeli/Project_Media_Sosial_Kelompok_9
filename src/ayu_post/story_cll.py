# ============================================================
# STORY CLL — Fitur Story menggunakan Circular Linked List
# Struktur data : Circular Linked List (CLL)
# Node terakhir selalu menunjuk kembali ke node PERTAMA (head)
# Fitur     :
#   1. Tambah story baru
#   2. Navigasi maju / mundur secara melingkar (tanpa ujung)
#   3. Tampilkan semua story
#   4. Hapus story berdasarkan posisi
# ============================================================

import os

_BASE_DIR   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STORY_FILE  = os.path.join(_BASE_DIR, "data", "stories.txt")


class StoryNode:
    """Node dalam Circular Linked List untuk satu story."""

    def __init__(self, username: str, teks: str):
        self.username = username
        self.teks     = teks
        self.next     = None   # pada CLL: node terakhir.next → head


class StoryCLL:
    """
    Circular Linked List untuk story.

    Struktur:
        head → [A] → [B] → [C] → (kembali ke A)
    Navigasi tidak pernah mentok — selalu melingkar.
    """

    def __init__(self):
        self.head    = None   # node pertama
        self.current = None   # posisi cursor navigasi saat ini
        self._size   = 0
        self._muat()

    # ── Muat dari file ──
    def _muat(self):
        try:
            with open(STORY_FILE, "r") as f:
                for baris in f:
                    baris = baris.strip()
                    if not baris:
                        continue
                    parts = baris.split("|", 1)
                    if len(parts) == 2:
                        self._append_internal(parts[0], parts[1])
        except FileNotFoundError:
            os.makedirs(os.path.dirname(STORY_FILE), exist_ok=True)
            open(STORY_FILE, "w").close()

    def _append_internal(self, username: str, teks: str):
        """Menambah node tanpa menyimpan ke file (dipakai saat muat)."""
        node = StoryNode(username, teks)
        if self.head is None:
            self.head    = node
            node.next    = self.head   # circular: tunjuk diri sendiri
            self.current = self.head
        else:
            # Temukan tail (node yang next-nya ke head)
            tail      = self.head
            while tail.next is not self.head:
                tail = tail.next
            tail.next = node
            node.next = self.head      # circular: tail baru tunjuk ke head
        self._size += 1

    # ── Tambah story baru ──
    def tambah_story(self, username: str, teks: str):
        """Menambah story baru dan menyimpan ke file."""
        self._append_internal(username, teks)

        os.makedirs(os.path.dirname(STORY_FILE), exist_ok=True)
        with open(STORY_FILE, "a") as f:
            f.write(f"{username}|{teks}\n")

        print(f"\n  [✓] Story berhasil ditambahkan!")
        print(f"      Total story sekarang: {self._size}")

    # ── Navigasi melingkar ──
    def next_story(self):
        """Geser ke story berikutnya (melingkar — tidak ada ujung)."""
        if self.is_empty():
            print("  [!] Belum ada story.")
            return
        self.current = self.current.next   # CLL: tidak perlu cek None
        self._cetak_story(self.current)

    def prev_story(self):
        """Geser ke story sebelumnya (traversal balik O(n) karena SLL arah)."""
        if self.is_empty():
            print("  [!] Belum ada story.")
            return

        # Cari node sebelum current dengan traversal O(n)
        temp = self.current
        while temp.next is not self.current:
            temp = temp.next
        self.current = temp
        self._cetak_story(self.current)

    def _cetak_story(self, node: StoryNode):
        print("\n  ┌─────────────────────────────────────┐")
        print(f"  │@{node.username:<35}│")
        print(f"  │  {node.teks:<35}│")
        print("  └─────────────────────────────────────┘")
        print("  [← prev]  [next →]  (navigasi melingkar / circular)")

    # ── Tampilkan semua story ──
    def tampilkan_semua(self):
        if self.is_empty():
            print("  [!] Belum ada story.")
            return

        print("\n╔══════════════════════════════════════════╗")
        print("║              SEMUA STORY                 ║")
        print("╚══════════════════════════════════════════╝")

        current = self.head
        nomor   = 1
        while True:
            marker = " ← (aktif)" if current is self.current else ""
            print(f"  {nomor}. @{current.username}: {current.teks}{marker}")
            current = current.next
            nomor  += 1
            if current is self.head:   # sudah melingkar penuh
                break

        print(f"\n  Total story: {self._size} (circular — navigasi tidak ada ujung)")

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self._size

    # ── Menu story ──
    def menu(self, username_login: str):
        """Menu interaktif untuk fitur Story."""
        if not self.is_empty():
            self.current = self.head   # reset ke awal

        while True:
            print("\n╔══════════════════════════════════════════╗")
            print("║              MENU STORY                  ║")
            print("╚══════════════════════════════════════════╝")
            print("  1. Buat Story Baru")
            print("  2. Lihat Semua Story")
            print("  3. Story Berikutnya →")
            print("  4. Story Sebelumnya ←")
            print("  0. Kembali")
            print("─" * 44)

            pilihan = input("  Pilihan: ").strip()

            if pilihan == "1":
                teks = input("\n  Isi story: ").strip()
                if teks:
                    self.tambah_story(username_login, teks)
                else:
                    print("  [!] Story tidak boleh kosong.")

            elif pilihan == "2":
                self.tampilkan_semua()

            elif pilihan == "3":
                self.next_story()

            elif pilihan == "4":
                self.prev_story()

            elif pilihan == "0":
                break

            else:
                print("  [!] Pilihan tidak valid.")
