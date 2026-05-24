# ============================================================
# UNDO SYSTEM — Stack untuk fitur buat & undo postingan
# Struktur data : Stack (LIFO) berbasis list Python
# Fitur     :
#   1. Buat post baru dan simpan ke file
#   2. Undo (hapus) post terakhir pada sesi ini
#   3. Lihat riwayat post sesi ini
# ============================================================

import os

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSTS_FILE = os.path.join(_BASE_DIR, "data", "posts.txt")


class Stack:
    """Stack sederhana berbasis list (LIFO)."""

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
    """Mengelola pembuatan dan undo postingan menggunakan Stack."""

    def __init__(self, username_login: str):
        self.username_login = username_login
        self.undo_stack     = Stack()

    def buat_post(self, caption: str):
        """Membuat post baru, menyimpan ke file, dan push ke stack undo."""
        post = {
            "username": self.username_login,
            "caption" : caption,
            "like"    : 0
        }

        os.makedirs(os.path.dirname(POSTS_FILE), exist_ok=True)

        try:
            with open(POSTS_FILE, "a") as f:
                f.write(f"{post['username']}|{post['caption']}|{post['like']}\n")
        except IOError:
            print("  [!] Gagal menyimpan postingan ke file.")
            return

        self.undo_stack.push(post)

        print("\n  [✓] Posting berhasil dibuat!")
        print(f"      Caption : {caption}")
        print(f"      Stack undo sekarang memiliki {self.undo_stack.size()} postingan.")

    def undo_post(self):
        """Menghapus post terakhir yang dibuat pada sesi ini."""
        if self.undo_stack.is_empty():
            print("  [!] Tidak ada postingan yang bisa di-undo pada sesi ini.")
            return

        post   = self.undo_stack.pop()
        target = f"{post['username']}|{post['caption']}|{post['like']}"

        try:
            with open(POSTS_FILE, "r") as f:
                semua = [b.strip() for b in f if b.strip()]

            # Hapus kemunculan terakhir dari baris yang cocok
            for i in range(len(semua) - 1, -1, -1):
                if semua[i] == target:
                    semua.pop(i)
                    break
            else:
                print("  [!] Postingan tidak ditemukan di file (mungkin sudah dihapus).")
                return

            with open(POSTS_FILE, "w") as f:
                for baris in semua:
                    f.write(baris + "\n")

            print(f"\n  [✓] Postingan berhasil di-undo!")
            print(f"      Caption yang dihapus: \"{post['caption']}\"")

        except FileNotFoundError:
            print("  [!] File posts.txt tidak ditemukan.")

    def lihat_riwayat(self):
        """Menampilkan semua post yang dibuat pada sesi ini (dari stack)."""
        if self.undo_stack.is_empty():
            print("  [!] Belum ada postingan yang dibuat pada sesi ini.")
            return

        items = self.undo_stack.semua_item()

        print("\n╔══════════════════════════════════════════╗")
        print("║         RIWAYAT POST SESI INI            ║")
        print("╚══════════════════════════════════════════╝")

        for i, post in enumerate(reversed(items), 1):
            label = "  ← (terbaru, bisa di-undo)" if i == 1 else ""
            print(f"  {i}. \"{post['caption']}\"{label}")
