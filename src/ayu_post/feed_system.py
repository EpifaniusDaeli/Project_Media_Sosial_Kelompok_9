class PostNode:
    def __init__(self, post_id: int, username: str, caption: str, like: int):
        self.post_id  = post_id  
        self.username = username
        self.caption  = caption
        self.like     = like
        self.prev     = None      
        self.next     = None      

    def __str__(self):
        return f"@{self.username}: {self.caption} | ❤ {self.like}"

class FeedDoubleLinkedList:
    def __init__(self):
        self.head = None   
        self.tail = None  
        self.size  = 0

    def append(self, post_id: int, username: str, caption: str, like: int):
        node = PostNode(post_id, username, caption, like)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev     = self.tail
            self.tail.next = node
            self.tail      = node
        self.size += 1

    # Tampilkan semua node dari head ke tail 
    def tampilkan(self) -> list:
        if self.is_empty():
            return []

        tampil = []
        current = self.head
        nomor   = 1

        while current is not None:
            print("=" * 38)
            print(f"  [{nomor}] @{current.username}")
            print(f"      {current.caption}")
            print(f"      ❤  {current.like} likes")
            print("=" * 38)
            tampil.append(current)
            current = current.next
            nomor  += 1

        return tampil

    # ── Searching: cari berdasarkan kata kunci caption ──
    def cari_caption(self, keyword: str) -> list:
        hasil   = []
        current = self.head

        while current is not None:
            if keyword.lower() in current.caption.lower():
                hasil.append(current)
            current = current.next

        return hasil

    # ── Searching: cari berdasarkan username ──
    def cari_username(self, username: str) -> list:
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
    file_posts = "data/posts.txt"

    def __init__(self, username_login: str, following: list):
        self.username_login = username_login
        self.following      = following          # list username yang di-follow
        self.feed           = FeedDoubleLinkedList()
        self._muat_feed()

    # ── Muat postingan dari file ke Double Linked List ──
    def _muat_feed(self):
        try:
            with open(self.file_posts, "r") as f:
                for idx, baris in enumerate(f):
                    baris = baris.strip()
                    if not baris:
                        continue

                    data = baris.split("|")
                    if len(data) < 3:
                        continue  # lewati baris yang formatnya tidak lengkap

                    username_post = data[0]
                    caption       = data[1]
                    like          = int(data[2]) if data[2].isdigit() else 0

                    # Filter: hanya tampilkan postingan yang relevan
                    if username_post in self.following or username_post == self.username_login:
                        self.feed.append(idx, username_post, caption, like)

        except FileNotFoundError:
            # Buat file kosong bila belum ada
            open(self.file_posts, "w").close()

    # ── Tampilkan feed ──
    def tampilkan_feed(self) -> list:
        if self.feed.is_empty():
            print("\n[!] Belum ada postingan di feed Anda.")
            return []

        print("\n╔══════════════════════════════════════╗")
        print("║          FEED POSTINGAN               ║")
        print("╚══════════════════════════════════════╝")

        return self.feed.tampilkan()

    # like postingan
    def like_post(self, posts: list, pilih: int):
        if pilih < 1 or pilih > len(posts):
            print("[!] Nomor postingan tidak valid.")
            return

        node = posts[pilih - 1]
        node.like += 1

        self._update_like_di_file(node)
        print(f"[✓] Berhasil like postingan @{node.username}!")
        print(f"    Total like sekarang: {node.like}")

    def _update_like_di_file(self, node: PostNode):
        try:
            with open(self.file_posts, "r") as f:
                semua = [b.strip().split("|") for b in f if b.strip()]

            # Update baris sesuai post_id node
            if 0 <= node.post_id < len(semua):
                semua[node.post_id][2] = str(node.like)

            with open(self.file_posts, "w") as f:
                for post in semua:
                    f.write("|".join(post) + "\n")

        except FileNotFoundError:
            print("[!] Gagal menyimpan perubahan like.")

    # caringan postingan
    def cari_postingan(self):
        print("\n=== CARI POSTINGAN ===")
        print("1. Cari berdasarkan kata kunci caption")
        print("2. Cari berdasarkan username")
        opsi = input("Pilihan: ")

        if opsi == "1":
            keyword = input("Masukkan kata kunci: ")
            hasil   = self.feed.cari_caption(keyword)
            label   = f"caption mengandung '{keyword}'"
        elif opsi == "2":
            uname = input("Masukkan username: ")
            hasil  = self.feed.cari_username(uname)
            label  = f"username '@{uname}'"
        else:
            print("[!] Pilihan tidak valid.")
            return

        if not hasil:
            print(f"[!] Tidak ada postingan dengan {label}.")
        else:
            print(f"\n=== Hasil Pencarian ({len(hasil)} ditemukan) ===")
            for i, node in enumerate(hasil, 1):
                print(f"  {i}. @{node.username}: {node.caption}  [❤ {node.like}]")

    # Menu utama FeedSystem
    def menu(self):
        while True:
            posts = self.tampilkan_feed()

            print("\n  1. Like postingan")
            print("  2. Cari postingan")
            print("  3. Kembali")
            pilihan = input("Pilihan: ")

            if pilihan == "1":
                if not posts:
                    continue
                try:
                    nomor = int(input("Like posting nomor: "))
                    self.like_post(posts, nomor)
                except ValueError:
                    print("[!] Masukkan angka yang valid.")

            elif pilihan == "2":
                self.cari_postingan()

            elif pilihan == "3":
                break

            else:
                print("[!] Pilihan tidak valid.")
