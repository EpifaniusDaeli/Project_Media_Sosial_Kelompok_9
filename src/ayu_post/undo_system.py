class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def semua_item(self) -> list:
        return list(self._data)


class UndoSystem:
    posts_file = "data/posts.txt"

    def __init__(self, username_login: str):
        self.username_login = username_login
        self.undo_stack     = Stack()

    def buat_post(self, caption: str):
        post = {
            "username": self.username_login,
            "caption" : caption,
            "like"    : 0
        }

        try:
            with open(self.posts_file, "a") as f:
                f.write(f"{post['username']}|{post['caption']}|{post['like']}\n")
        except IOError:
            print("[!] Gagal menyimpan postingan ke file.")
            return

        self.undo_stack.push(post)

        print("\n[✓] Posting berhasil dibuat!")
        print(f"    Caption : {caption}")
        print(f"    Stack undo sekarang memiliki {self.undo_stack.size()} postingan.")

    def undo_post(self):
        if self.undo_stack.is_empty():
            print("[!] Tidak ada postingan yang bisa di-undo pada sesi ini.")
            return

        post   = self.undo_stack.pop()
        target = f"{post['username']}|{post['caption']}|{post['like']}"

        try:
            with open(self.posts_file, "r") as f:
                semua = [b.strip() for b in f if b.strip()]

            for i in range(len(semua) - 1, -1, -1):
                if semua[i] == target:
                    semua.pop(i)
                    break
            else:
                print("[!] Postingan tidak ditemukan di file (mungkin sudah dihapus).")
                return

            with open(self.posts_file, "w") as f:
                for baris in semua:
                    f.write(baris + "\n")

            print(f"\n[✓] Postingan berhasil di-undo!")
            print(f"    Caption yang dihapus: \"{post['caption']}\"")

        except FileNotFoundError:
            print("[!] File posts.txt tidak ditemukan.")

    def lihat_riwayat(self):
        if self.undo_stack.is_empty():
            print("[!] Belum ada postingan yang dibuat pada sesi ini.")
            return

        items = self.undo_stack.semua_item()

        print("\n╔══════════════════════════════════════╗")
        print("║        RIWAYAT POST SESI INI          ║")
        print("╚══════════════════════════════════════╝")

        for i, post in enumerate(reversed(items), 1):
            label = " ← (terbaru, bisa di-undo)" if i == 1 else ""
            print(f"  {i}. \"{post['caption']}\"{label}")

    def menu(self):
        while True:
            print("\n╔══════════════════════════════════════╗")
            print("║            MENU POSTINGAN             ║")
            print("╚══════════════════════════════════════╝")
            print("  1. Buat Post Baru")
            print("  2. Undo Post Terakhir")
            print("  3. Lihat Riwayat Post Sesi Ini")
            print("  4. Kembali")

            pilihan = input("Pilihan: ")

            if pilihan == "1":
                caption = input("Masukkan caption: ").strip()
                if caption:
                    self.buat_post(caption)
                else:
                    print("[!] Caption tidak boleh kosong.")

            elif pilihan == "2":
                self.undo_post()

            elif pilihan == "3":
                self.lihat_riwayat()

            elif pilihan == "4":
                break

            else:
                print("[!] Pilihan tidak valid.")
