POST_FILE = "data/posts.txt"

class CircularNode:
    """Satu node dalam Circular Linked List."""

    def __init__(self, post_id: int, username: str, caption: str, like: int):
        self.post_id  = post_id
        self.username = username
        self.caption  = caption
        self.like     = like
        self.next     = None  

class CircularFeed:
    def __init__(self):
        self.head    = None
        self.tail    = None
        self.current = None   
        self.size    = 0

    # append
    def tambah(self, post_id: int, username: str, caption: str, like: int):
        """Tambah postingan di akhir, lalu sambungkan tail ke head"""
        node = CircularNode(post_id, username, caption, like)

        if self.head is None:
            # List kosong: satu node melingkar ke dirinya sendiri
            self.head    = node
            self.tail    = node
            node.next    = node      
            self.current = node
        else:
            # Sisipkan setelah tail yang lama
            self.tail.next = node   
            self.tail      = node
            node.next      = self.head   

        self.size += 1

    # Load dari file
    def muat_dari_file(self, following: list, username_login: str):
        """Baca posts.txt dan filter hanya postingan yang relevan."""
        try:
            with open(POST_FILE, "r") as f:
                for idx, baris in enumerate(f):
                    baris = baris.strip()
                    if not baris:
                        continue
                    data = baris.split("|")
                    if len(data) < 3:
                        continue

                    uname  = data[0]
                    caption = data[1]
                    like    = int(data[2]) if data[2].isdigit() else 0

                    # Tampilkan postingan sendiri + postingan yang difollow
                    if uname in following or uname == username_login:
                        self.tambah(idx, uname, caption, like)

        except FileNotFoundError:
            open(POST_FILE, "w").close()

    # ── TAMPILKAN SATU NODE ──
    def _tampilkan_node(self, node: CircularNode, posisi: int):
        print("\n" + "═" * 42)
        print(f"  Postingan {posisi} / {self.size}  [Circular Browse]")
        print("─" * 42)
        print(f"  👤  @{node.username}")
        print(f"  📝  {node.caption}")
        print(f"  ❤   {node.like} likes")
        print("═" * 42)
        print("  [N] Next   [P] Prev   [Q] Keluar")

    # ── BROWSE INTERAKTIF ──
    def browse(self):
        """
        Browse melingkar: N = maju ke next, P = mundur ke prev.
        Karena circular, setelah node terakhir otomatis kembali ke node pertama.
        """
        if self.head is None:
            print("\n[!] Tidak ada postingan untuk di-browse.")
            return

        self.current = self.head
        posisi       = 1

        while True:
            self._tampilkan_node(self.current, posisi)
            aksi = input("  Aksi: ").strip().lower()

            if aksi == "n":
                # Maju
                self.current = self.current.next
                posisi = (posisi % self.size) + 1

            elif aksi == "p":
                # Mundur
                prev = self.current
                while prev.next != self.current:
                    prev = prev.next
                self.current = prev
                posisi = posisi - 1 if posisi > 1 else self.size

            elif aksi == "q":
                print("\n[←] Keluar dari mode browse.")
                break

            else:
                print("[!] Pilihan tidak valid.")

    # Menu
    def menu(self, following: list, username_login: str):
        """Reset lalu muat ulang data, kemudian jalankan browse."""
        self.__init__()   # reset agar data selalu fresh
        self.muat_dari_file(following, username_login)

        print("\n╔══════════════════════════════════════════╗")
        print("║     BROWSE POSTINGAN — Circular Feed     ║")
        print("╚══════════════════════════════════════════╝")

        if self.size == 0:
            print("[!] Belum ada postingan untuk di-browse.")
            return

        print(f"  Total postingan tersedia: {self.size}")
        self.browse()
