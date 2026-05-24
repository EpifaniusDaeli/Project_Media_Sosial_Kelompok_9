# ============================================================
# MAIN PROGRAM — Social Media CLI
# Anggota:
#   - Epifanius  : Sistem autentikasi (login, register)
#   - Ayu        : Sistem posting (buat post, feed, komentar)
#   - Salsabila  : Sistem sosial (follow, chat, sorting user)
# ============================================================

import os
import sys

# Tambahkan direktori src ke path agar import modul berjalan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ── Import modul autentikasi (Epi) ──
from epifanius_auth.auth_system    import login, register
from epifanius_auth.login_history  import tampilkan_history

# ── Import modul posting & feed (Ayu) ──
from ayu_post.undo_system  import UndoSystem
from ayu_post.feed_system  import FeedSystem

# ── Import modul sosial (Salsabila) ──
from salsabila_social.follow_graph  import (
    follow_user, unfollow_user,
    show_following, show_followers,
    load_follow_data
)
from salsabila_social.sistem_chat   import send_message, show_chat
from salsabila_social.sorting_menu  import sort_ascending, sort_descending, search_user

# Path absolut ke file users
_BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(_BASE_DIR, "..", "data", "users.txt")


# ════════════════════════════════════════════════════════════
# UTILITAS
# ════════════════════════════════════════════════════════════

def ambil_semua_username() -> list:
    """Membaca semua username terdaftar dari file."""
    usernames = []
    if not os.path.exists(USERS_FILE):
        return usernames
    with open(USERS_FILE, "r") as f:
        for baris in f:
            baris = baris.strip()
            if baris:
                usernames.append(baris.split(",")[0])
    return usernames


def ambil_following(username: str) -> list:
    """Membaca daftar user yang di-follow oleh username."""
    graph = load_follow_data()
    return graph.get(username, [])


def cetak_judul(teks: str):
    """Mencetak header dengan border."""
    lebar = 42
    print("\n╔" + "═" * lebar + "╗")
    print("║" + teks.center(lebar) + "║")
    print("╚" + "═" * lebar + "╝")


# ════════════════════════════════════════════════════════════
# MENU POSTING (Ayu)
# ════════════════════════════════════════════════════════════

def menu_posting(username_login: str):
    """
    Menu postingan:
      1. Buat Post Baru
      2. Undo Post Terakhir
      3. Riwayat Post Sesi Ini
      4. Lihat Feed, Like & Komentar
    """
    undo_sys = UndoSystem(username_login)

    while True:
        cetak_judul("MENU POSTINGAN")
        print("  1. Buat Post Baru")
        print("  2. Undo Post Terakhir")
        print("  3. Riwayat Post Sesi Ini")
        print("  4. Lihat Feed, Like & Komentar")
        print("  0. Kembali")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            caption = input("\n  Masukkan caption: ").strip()
            if caption:
                undo_sys.buat_post(caption)
            else:
                print("  [!] Caption tidak boleh kosong.")

        elif pilihan == "2":
            undo_sys.undo_post()

        elif pilihan == "3":
            undo_sys.lihat_riwayat()

        elif pilihan == "4":
            following = ambil_following(username_login)
            feed_sys  = FeedSystem(username_login, following)
            feed_sys.menu(username_login)

        elif pilihan == "0":
            break

        else:
            print("  [!] Pilihan tidak valid.")


# ════════════════════════════════════════════════════════════
# MENU SOSIAL (Salsabila)
# ════════════════════════════════════════════════════════════

def menu_sosial(username_login: str):
    """Menu sosial: follow, chat, sorting, cari user."""
    daftar_user = ambil_semua_username()

    while True:
        cetak_judul("MENU SOSIAL MEDIA")
        print(f"  Login sebagai : {username_login}")
        print("─" * 44)
        print("  1. Follow User")
        print("  2. Unfollow User")
        print("  3. Lihat Following")
        print("  4. Lihat Followers")
        print("  5. Kirim Pesan (Chat)")
        print("  6. Lihat Riwayat Chat")
        print("  7. Urutkan User (A-Z / Z-A)")
        print("  8. Cari User")
        print("  0. Kembali")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            target = input("\n  Username yang ingin di-follow: ").strip()
            follow_user(username_login, target)

        elif pilihan == "2":
            target = input("\n  Username yang ingin di-unfollow: ").strip()
            unfollow_user(username_login, target)

        elif pilihan == "3":
            show_following(username_login)

        elif pilihan == "4":
            show_followers(username_login)

        elif pilihan == "5":
            penerima = input("\n  Kirim pesan ke (username): ").strip()
            pesan    = input("  Isi pesan               : ").strip()
            send_message(username_login, penerima, pesan)

        elif pilihan == "6":
            show_chat(username_login)

        elif pilihan == "7":
            print("\n  Urutkan berdasarkan:")
            print("  1. A-Z (Ascending)")
            print("  2. Z-A (Descending)")
            sub = input("  Pilihan: ").strip()

            if sub == "1":
                hasil = sort_ascending(daftar_user)
                label = "A-Z"
            elif sub == "2":
                hasil = sort_descending(daftar_user)
                label = "Z-A"
            else:
                print("  [!] Pilihan tidak valid.")
                continue

            print(f"\n  Daftar User ({label}):")
            for i, u in enumerate(hasil, 1):
                print(f"    {i}. {u}")

        elif pilihan == "8":
            keyword = input("\n  Kata kunci pencarian: ").strip()
            hasil   = search_user(daftar_user, keyword)

            print(f"\n  Hasil pencarian '{keyword}':")
            if hasil:
                for i, u in enumerate(hasil, 1):
                    print(f"    {i}. {u}")
            else:
                print("  (tidak ditemukan)")

        elif pilihan == "0":
            break

        else:
            print("  [!] Pilihan tidak valid.")


# ════════════════════════════════════════════════════════════
# MENU UTAMA USER (setelah login)
# ════════════════════════════════════════════════════════════

def menu_user(username_login: str):
    """Menu utama setelah user berhasil login."""
    while True:
        cetak_judul(f"SELAMAT DATANG, {username_login.upper()}")
        print("  1. Postingan  (Buat, Feed, Like & Komentar)")
        print("  2. Sosial     (Follow, Chat, Cari User)")
        print("  3. Riwayat Login")
        print("  0. Logout")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            menu_posting(username_login)

        elif pilihan == "2":
            menu_sosial(username_login)

        elif pilihan == "3":
            tampilkan_history(username_login)

        elif pilihan == "0":
            print(f"\n  [✓] {username_login} berhasil logout. Sampai jumpa!\n")
            break

        else:
            print("  [!] Pilihan tidak valid.")


# ════════════════════════════════════════════════════════════
# MENU AWAL (Sebelum Login)
# ════════════════════════════════════════════════════════════

def main():
    """Titik masuk utama program."""
    while True:
        cetak_judul("SOCIAL MEDIA APP")
        print("  1. Login")
        print("  2. Register")
        print("  0. Keluar")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            user = login()
            if user is not None:
                menu_user(user.username)

        elif pilihan == "2":
            register()

        elif pilihan == "0":
            print("\n  Program selesai. Terima kasih!\n")
            break

        else:
            print("  [!] Pilihan tidak valid.")


# ── Entry point ──
if __name__ == "__main__":
    main()
