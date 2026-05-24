# ============================================================
# COMMENT TREE — Pohon komentar berbasis rekursi
# Struktur data : Tree (N-ary) dengan dictionary sebagai indeks
# Fitur     :
#   1. Muat komentar dari file (format: id|post_id|parent_id|user|teks)
#   2. Tambah komentar baru (root) atau balasan (child)
#   3. Tampilkan komentar secara rekursif (thread)
#   4. Hitung total komentar secara rekursif
# ============================================================

import os

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KOMEN_FILE  = os.path.join(_BASE_DIR, "data", "komentar.txt")


class CommentNode:
    """Node dalam Comment Tree yang mewakili satu komentar."""

    def __init__(self, comment_id: int, post_id: int,
                 parent_id: int, username: str, teks: str):
        self.comment_id = comment_id   # ID unik komentar
        self.post_id    = post_id      # ID post yang dikomentari
        self.parent_id  = parent_id    # -1 jika komentar root
        self.username   = username     # Penulis komentar
        self.teks       = teks         # Isi komentar
        self.children   = []           # Daftar balasan

    def __str__(self):
        return f"[{self.comment_id}] @{self.username}: {self.teks}"


class CommentTree:
    """Pohon komentar untuk satu postingan."""

    def __init__(self, post_id: int):
        self.post_id  = post_id
        self.nodes    = {}    # comment_id → CommentNode
        self.roots    = []    # komentar tanpa parent
        self._next_id = 1     # auto-increment ID
        self.muat_komentar()

    # ── Muat komentar dari file ──
    def muat_komentar(self):
        """Membaca semua komentar dari file dan membangun pohon untuk post ini."""
        try:
            with open(KOMEN_FILE, "r") as f:
                for baris in f:
                    baris = baris.strip()
                    if not baris:
                        continue

                    data = baris.split("|", 4)
                    if len(data) < 5:
                        continue

                    try:
                        comment_id = int(data[0])
                        post_id    = int(data[1])
                        parent_id  = int(data[2])
                        username   = data[3]
                        teks       = data[4]
                    except ValueError:
                        continue   # lewati baris yang rusak

                    # Perbarui auto-increment
                    if comment_id >= self._next_id:
                        self._next_id = comment_id + 1

                    node = CommentNode(comment_id, post_id, parent_id, username, teks)
                    self.nodes[comment_id] = node

            # Bangun struktur pohon hanya untuk post ini
            for node in self.nodes.values():
                if node.post_id != self.post_id:
                    continue   # komentar milik post lain

                if node.parent_id == -1:
                    self.roots.append(node)
                elif node.parent_id in self.nodes:
                    self.nodes[node.parent_id].children.append(node)

        except FileNotFoundError:
            # Buat file kosong jika belum ada
            os.makedirs(os.path.dirname(KOMEN_FILE), exist_ok=True)
            open(KOMEN_FILE, "w").close()

    # ── Tambah komentar baru ──
    def tambah_komentar(self, username: str, teks: str, parent_id: int = -1):
        """
        Menambahkan komentar baru.

        Args:
            username  : penulis komentar
            teks      : isi komentar
            parent_id : ID komentar yang dibalas (-1 jika komentar baru)
        """
        comment_id     = self._next_id
        self._next_id += 1

        # Validasi parent_id
        if parent_id != -1 and parent_id not in self.nodes:
            print(f"  [!] Komentar ID {parent_id} tidak ada. Dijadikan komentar baru.")
            parent_id = -1

        node = CommentNode(comment_id, self.post_id, parent_id, username, teks)
        self.nodes[comment_id] = node

        if parent_id == -1:
            self.roots.append(node)
        else:
            self.nodes[parent_id].children.append(node)

        # Simpan ke file (append)
        try:
            with open(KOMEN_FILE, "a") as f:
                f.write(f"{comment_id}|{self.post_id}|{parent_id}|{username}|{teks}\n")
            print(f"\n  [✓] Komentar berhasil ditambahkan! (ID: {comment_id})")
        except IOError:
            print("  [!] Gagal menyimpan komentar ke file.")

    # ── Tampilkan komentar secara rekursif ──
    def _tampilkan_rekursif(self, node: CommentNode, level: int = 0):
        indent = "    " * level
        simbol = "●" if level == 0 else ("└─" if level == 1 else "  └─")

        print(f"{indent}{simbol} @{node.username} [ID:{node.comment_id}]")
        print(f"{indent}   {node.teks}")

        for child in node.children:
            self._tampilkan_rekursif(child, level + 1)

    def tampilkan_semua(self):
        """Menampilkan seluruh pohon komentar untuk post ini."""
        if not self.roots:
            print("\n  [!] Belum ada komentar pada postingan ini.")
            return

        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║   KOMENTAR POSTINGAN (Post #{self.post_id:<6})      ║")
        print(f"╚══════════════════════════════════════════╝")

        for root in self.roots:
            self._tampilkan_rekursif(root)
            print()   # baris kosong antar-thread komentar

        print(f"  Total komentar: {self.hitung_semua()}")

    # ── Hitung total komentar secara rekursif ──
    def _hitung_rekursif(self, node: CommentNode) -> int:
        total = 1   # hitung node ini sendiri
        for child in node.children:
            total += self._hitung_rekursif(child)
        return total

    def hitung_semua(self) -> int:
        """Mengembalikan total jumlah komentar (termasuk balasan)."""
        return sum(self._hitung_rekursif(root) for root in self.roots)

    def cari_id(self, comment_id: int):
        """Mencari komentar berdasarkan ID."""
        return self.nodes.get(comment_id, None)

    def tampilkan_thread(self, comment_id: int):
        """Menampilkan satu thread komentar mulai dari ID tertentu."""
        node = self.cari_id(comment_id)
        if node is None:
            print(f"  [!] Komentar ID {comment_id} tidak ditemukan.")
            return

        print(f"\n  Thread komentar (mulai dari ID {comment_id}):")
        self._tampilkan_rekursif(node)

    # ── Menu utama CommentTree ──
    def menu(self, username_login: str):
        """Menu interaktif untuk mengelola komentar."""
        while True:
            print(f"\n╔══════════════════════════════════════════╗")
            print(f"║            MENU KOMENTAR                 ║")
            print(f"╚══════════════════════════════════════════╝")
            print("  1. Lihat Semua Komentar")
            print("  2. Tambah Komentar Baru")
            print("  3. Balas Komentar")
            print("  4. Lihat Thread Komentar")
            print("  0. Kembali")
            print("─" * 44)

            pilihan = input("  Pilihan: ").strip()

            if pilihan == "1":
                self.tampilkan_semua()

            elif pilihan == "2":
                teks = input("  Tulis komentar: ").strip()
                if teks:
                    self.tambah_komentar(username_login, teks)
                else:
                    print("  [!] Komentar tidak boleh kosong.")

            elif pilihan == "3":
                self.tampilkan_semua()
                try:
                    parent_id = int(input("  Masukkan ID komentar yang ingin dibalas: "))
                    node      = self.cari_id(parent_id)
                    if node is None:
                        print(f"  [!] Komentar ID {parent_id} tidak ditemukan.")
                    else:
                        print(f"  Membalas: @{node.username}: {node.teks}")
                        teks = input("  Tulis balasan: ").strip()
                        if teks:
                            self.tambah_komentar(username_login, teks, parent_id)
                        else:
                            print("  [!] Balasan tidak boleh kosong.")
                except ValueError:
                    print("  [!] Masukkan angka yang valid.")

            elif pilihan == "4":
                try:
                    comment_id = int(input("  Masukkan ID komentar: "))
                    self.tampilkan_thread(comment_id)
                except ValueError:
                    print("  [!] Masukkan angka yang valid.")

            elif pilihan == "0":
                break

            else:
                print("  [!] Pilihan tidak valid.")
