# ============================================================
# FEED SYSTEM — Double Linked List untuk postingan
# Struktur data : Double Linked List
# Fitur     :
#   1. Muat feed dari file (posts milik sendiri + following)
#   2. Tampilkan feed beserta komentar tiap post
#   3. Like postingan (memicu notifikasi SLL)
#   4. Tambah komentar / balas komentar (memicu notifikasi SLL)
#   5. Cari postingan berdasarkan caption atau username
# ============================================================

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ayu_post.comment_tree import CommentTree

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSTS_FILE = os.path.join(_BASE_DIR, "data", "posts.txt")


class PostNode:
    """Node dalam Double Linked List yang mewakili satu postingan."""

    def __init__(self, post_id: int, username: str, caption: str, like: int):
        self.post_id  = post_id
        self.username = username
        self.caption  = caption
        self.like     = like
        self.prev     = None   # pointer ke node sebelumnya (DLL)
        self.next     = None   # pointer ke node berikutnya (DLL)

    def __str__(self):
        return f"@{self.username}: {self.caption} | ❤ {self.like}"


class FeedDoubleLinkedList:
    """Double Linked List untuk menyimpan dan menampilkan feed postingan."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size  = 0

    def append(self, post_id: int, username: str, caption: str, like: int):
        """Menambahkan node baru di akhir list (tail)."""
        node = PostNode(post_id, username, caption, like)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev      = self.tail   # DLL: sambungkan prev
            self.tail.next = node
            self.tail      = node
        self.size += 1

    def tampilkan(self) -> list:
        """Tampilkan semua post beserta komentar masing-masing."""
        if self.is_empty():
            return []

        tampil  = []
        current = self.head
        nomor   = 1

        while current is not None:
            print("\n" + "═" * 44)
            print(f"  [{nomor}] @{current.username}")
            print(f"       {current.caption}")
            print(f"       ❤  {current.like} likes")
            print("─" * 44)

            # Tampilkan komentar langsung di bawah post
            tree = CommentTree(current.post_id)
            if not tree.roots:
                print("  💬 Belum ada komentar.")
            else:
                print(f"  💬 Komentar ({tree.hitung_semua()}):")
                for root in tree.roots:
                    tree._tampilkan_rekursif(root, level=0)

            print("═" * 44)
            tampil.append(current)
            current = current.next
            nomor  += 1

        return tampil

    def cari_caption(self, keyword: str) -> list:
        """Mencari post yang caption-nya mengandung keyword."""
        hasil   = []
        current = self.head
        while current is not None:
            if keyword.lower() in current.caption.lower():
                hasil.append(current)
            current = current.next
        return hasil

    def cari_username(self, username: str) -> list:
        """Mencari semua post milik username tertentu."""
        hasil   = []
        current = self.head
        while current is not None:
            if current.username.lower() == username.lower():
                hasil.append(current)
            current = current.next
        return hasil

    def is_empty(self) -> bool:
        return self.head is None


class FeedSystem:
    """Sistem feed yang memuat dan mengelola postingan dari file."""

    def __init__(self, username_login: str, following: list):
        self.username_login = username_login
        self.following      = following
        self.feed           = FeedDoubleLinkedList()
        self._muat_feed()

    def _muat_feed(self):
        """Memuat postingan dari file ke Double Linked List."""
        try:
            with open(POSTS_FILE, "r") as f:
                for idx, baris in enumerate(f):
                    baris = baris.strip()
                    if not baris:
                        continue
                    data = baris.split("|")
                    if len(data) < 3:
                        continue
                    username_post = data[0]
                    caption       = data[1]
                    like          = int(data[2]) if data[2].isdigit() else 0

                    # Tampilkan post milik sendiri atau yang di-follow
                    if username_post in self.following or username_post == self.username_login:
                        self.feed.append(idx, username_post, caption, like)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(POSTS_FILE), exist_ok=True)
            open(POSTS_FILE, "w").close()

    def tampilkan_feed(self) -> list:
        """Menampilkan semua postingan di feed."""
        if self.feed.is_empty():
            print("\n  [!] Belum ada postingan di feed Anda.")
            return []

        print("\n╔══════════════════════════════════════════╗")
        print("║           FEED POSTINGAN                 ║")
        print("╚══════════════════════════════════════════╝")

        return self.feed.tampilkan()

    def like_post(self, posts: list, pilih: int, notif=None):
        """Menambah satu like pada postingan yang dipilih."""
        if pilih < 1 or pilih > len(posts):
            print("  [!] Nomor postingan tidak valid.")
            return
        node = posts[pilih - 1]
        node.like += 1
        self._update_like_di_file(node)
        print(f"\n  [✓] Berhasil like postingan @{node.username}!")
        print(f"      Total like sekarang: {node.like}")

        # Tambahkan notifikasi ke SLL
        if notif is not None:
            notif.tambah(f"@{self.username_login} menyukai post @{node.username}")

    def _update_like_di_file(self, node: PostNode):
        """Memperbarui jumlah like sebuah post di file."""
        try:
            with open(POSTS_FILE, "r") as f:
                semua = [b.strip().split("|") for b in f if b.strip()]
            if 0 <= node.post_id < len(semua):
                semua[node.post_id][2] = str(node.like)
            with open(POSTS_FILE, "w") as f:
                for post in semua:
                    f.write("|".join(post) + "\n")
        except FileNotFoundError:
            print("  [!] Gagal menyimpan perubahan like.")

    def komentar_post(self, posts: list, pilih: int, username_login: str, notif=None):
        """Membuka menu komentar untuk post yang dipilih."""
        if pilih < 1 or pilih > len(posts):
            print("  [!] Nomor postingan tidak valid.")
            return
        node = posts[pilih - 1]
        print(f"\n  Postingan @{node.username}: \"{node.caption}\"")
        tree = CommentTree(node.post_id)
        tree.menu(username_login)

        # Tambahkan notifikasi ke SLL setelah keluar menu komentar
        if notif is not None:
            notif.tambah(f"@{username_login} mengomentari post @{node.username}")

    def cari_postingan(self):
        """Menu pencarian postingan berdasarkan caption atau username."""
        print("\n╔══════════════════════════════════════════╗")
        print("║           CARI POSTINGAN                 ║")
        print("╚══════════════════════════════════════════╝")
        print("  1. Cari berdasarkan kata kunci caption")
        print("  2. Cari berdasarkan username")
        print("─" * 44)
        opsi = input("  Pilihan: ").strip()

        if opsi == "1":
            keyword = input("  Masukkan kata kunci: ").strip()
            hasil   = self.feed.cari_caption(keyword)
            label   = f"caption mengandung '{keyword}'"
        elif opsi == "2":
            uname  = input("  Masukkan username: ").strip()
            hasil  = self.feed.cari_username(uname)
            label  = f"username '@{uname}'"
        else:
            print("  [!] Pilihan tidak valid.")
            return

        if not hasil:
            print(f"\n  [!] Tidak ada postingan dengan {label}.")
        else:
            print(f"\n  Hasil Pencarian ({len(hasil)} ditemukan):")
            for i, node in enumerate(hasil, 1):
                print(f"    {i}. @{node.username}: {node.caption}  [❤ {node.like}]")

    def menu(self, username_login: str, notif=None):
        """Menu feed: tampilkan post+komentar, like, komentar, cari."""
        while True:
            posts = self.tampilkan_feed()

            print("\n  1. Like postingan")
            print("  2. Komentar postingan")
            print("  3. Cari postingan")
            print("  0. Kembali")
            print("─" * 44)
            pilihan = input("  Pilihan: ").strip()

            if pilihan == "1":
                if not posts:
                    continue
                try:
                    nomor = int(input("  Like posting nomor: "))
                    self.like_post(posts, nomor, notif)
                except ValueError:
                    print("  [!] Masukkan angka yang valid.")

            elif pilihan == "2":
                if not posts:
                    continue
                try:
                    nomor = int(input("  Pilih nomor post untuk dikomentari: "))
                    self.komentar_post(posts, nomor, username_login, notif)
                except ValueError:
                    print("  [!] Masukkan angka yang valid.")

            elif pilihan == "3":
                self.cari_postingan()

            elif pilihan == "0":
                break

            else:
                print("  [!] Pilihan tidak valid.")
