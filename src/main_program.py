# ============================================================
# MAIN PROGRAM — SOSIAL MEDIA CLI (INTEGRASI SISTEM)
# ============================================================

import os
import sys

# Tambahkan direktori src ke path agar import modul berjalan lancar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Modul Autentikasi (Epifanius) ──
from epifanius_auth.auth_system import login, register
from epifanius_auth.login_history import tampilkan_history
from epifanius_auth.user_hash import HashTable

# ── Modul Posting & Feed (Ayu) ──
from ayu_post.undo_system import UndoSystem
from ayu_post.feed_system import FeedSystem
from ayu_post.notif_sll import NotifSLL
from ayu_post.story_cll import StoryCLL

# ── Modul Sosial & Chat (Salsabila) ──
from salsabila_social.follow_graph import (
    follow_user, unfollow_user,
    show_following, show_followers,
    load_follow_data
)
from salsabila_social.sistem_chat import send_message, show_chat
from salsabila_social.sorting_menu import sort_ascending, sort_descending, search_user

# Path file teks data user
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(_BASE_DIR, "..", "data", "users.txt")


# ════════════════════════════════════════════════════════════
# FUNGSI UTILITAS / PEMBANTU
# ════════════════════════════════════════════════════════════

def ambil_semua_username():
    usernames = []
    if not os.path.exists(USERS_FILE):
        return usernames
    with open(USERS_FILE, "r") as f:
        for baris in f:
            baris = baris.strip()
            if baris:
                usernames.append(baris.split(",")[0])
    return usernames


def ambil_following(username):
    graph = load_follow_data()
    if username in graph:
        return graph[username]
    return []


def cetak_judul(teks):
    lebar = 42
    print("\n╔" + "═" * lebar + "╗")
    print("║" + teks.center(lebar) + "║")
    print("╚" + "═" * lebar + "╝")


# ════════════════════════════════════════════════════════════
# MENU UTAMA POSTINGAN (Ayu)
# ════════════════════════════════════════════════════════════

def menu_posting(username_login, notif):
    undo_sys = UndoSystem(username_login)
    story_cll = StoryCLL()

    while True:
        cetak_judul("MENU POSTINGAN")
        print("  1. Buat Post Baru")
        print("  2. Undo Post Terakhir")
        print("  3. Riwayat Post Sesi Ini")
        print("  4. Lihat Feed, Like & Komentar")
        print("  5. Story")
        print("  6. Notifikasi")
        print("  0. Kembali")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            caption = input("\n  Masukkan caption: ").strip()
            if caption:
                undo_sys.buat_post(caption)
                notif.tambah(f"Post baru oleh @{username_login}: \"{caption[:30]}\"")
            else:
                print("  [!] Caption tidak boleh kosong.")

        elif pilihan == "2":
            undo_sys.undo_post()

        elif pilihan == "3":
            undo_sys.lihat_riwayat()

        elif pilihan == "4":
            following = ambil_following(username_login)
            feed_sys = FeedSystem(username_login, following)
            feed_sys.menu(username_login, notif)

        elif pilihan == "5":
            story_cll.menu(username_login)

        elif pilihan == "6":
            notif.tampilkan(username_login)
            if not notif.is_empty():
                hapus = input("\n  Hapus notifikasi terlama? (y/n): ").strip().lower()
                if hapus == "y":
                    notif.hapus_terlama()

        elif pilihan == "0":
            break
        else:
            print("  [!] Pilihan tidak valid.")


# ════════════════════════════════════════════════════════════
# MENU UTAMA SOSIAL (Salsabila)
# ════════════════════════════════════════════════════════════

def menu_sosial(username_login):
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
            pesan = input("  Isi pesan               : ").strip()
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
            for i in range(len(hasil)):
                print(f"    {i+1}. {hasil[i]}")

        elif pilihan == "8":
            keyword = input("\n  Kata kunci pencarian: ").strip()
            hasil = search_user(daftar_user, keyword)

            print(f"\n  Hasil pencarian '{keyword}':")
            if hasil:
                for i in range(len(hasil)):
                    print(f"    {i+1}. {hasil[i]}")
            else:
                print("  (tidak ditemukan)")

        elif pilihan == "0":
            break
        else:
            print("  [!] Pilihan tidak valid.")


# ════════════════════════════════════════════════════════════
# MENU TESTING HASH TABLE (Bagian Edukasi Milik Epi)
# ════════════════════════════════════════════════════════════

def menu_hash_table():
    usernames = ambil_semua_username()
    if not usernames:
        print("\n  [!] Belum ada user terdaftar.")
        return

    # Memanggil method untuk membangun hash table dari array usernames
    tabel = HashTable(ukuran=max(16, len(usernames) * 2))
    for u in usernames:
        tabel.insert(u, u)
    tabel.tampilkan()


# ════════════════════════════════════════════════════════════
# DASHBOARD UTAMA SETELAH LOGIN
# ════════════════════════════════════════════════════════════

def menu_user(username_login):
    # Membuat objek struktur data Single Linked List untuk menampung notifikasi sesi ini
    notif = NotifSLL()
    notif.tambah(f"Selamat datang kembali, @{username_login}!")

    while True:
        cetak_judul(f"SELAMAT DATANG, {username_login.upper()}")
        print("  1. Postingan  (Buat, Feed, Story, Notifikasi)")
        print("  2. Sosial     (Follow, Chat, Cari User)")
        print("  3. Riwayat Login")
        print("  4. Lihat Hash Table User")
        print("  0. Logout")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            menu_posting(username_login, notif)

        elif pilihan == "2":
            menu_sosial(username_login)

        elif pilihan == "3":
            tampilkan_history(username_login)

        elif pilihan == "4":
            menu_hash_table()

        elif pilihan == "0":
            print(f"\n  [✓] {username_login} berhasil logout. Sampai jumpa!\n")
            break
        else:
            print("  [!] Pilihan tidak valid.")


# ════════════════════════════════════════════════════════════
# ENTRY POINT UTAMA
# ════════════════════════════════════════════════════════════

def main():
    while True:
        cetak_judul("SOCIAL MEDIA APP")
        print("  1. Login")
        print("  2. Register")
        print("  0. Keluar")
        print("─" * 44)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            user = login()
            # Jika login sukses (mengembalikan objek User)
            if user is not None:
                menu_user(user.username)

        elif pilihan == "2":
            register()

        elif pilihan == "0":
            print("\n  Program selesai. Terima kasih!\n")
            break
        else:
            print("  [!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()