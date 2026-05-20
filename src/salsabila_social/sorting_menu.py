# ============================================================
# ALGORITMA: Bubble Sort
# Membandingkan dua elemen bersebelahan dan menukar jika perlu.
# Kompleksitas: O(n²) — cocok untuk data kecil dan mudah dijelaskan.
# ============================================================

def sort_ascending(data):
    """Mengurutkan daftar username dari A ke Z menggunakan Bubble Sort."""
    arr = data.copy()  # salin agar data asli tidak berubah
    n = len(arr)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            # Bandingkan dua elemen bersebelahan
            if arr[j] > arr[j + 1]:
                # Tukar posisi jika urutan salah
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def sort_descending(data):
    """Mengurutkan daftar username dari Z ke A menggunakan Bubble Sort."""
    # Gunakan hasil ascending lalu balik urutannya
    return sort_ascending(data)[::-1]


def search_user(data, keyword):
    """Mencari user yang mengandung keyword (tidak peka huruf besar/kecil)."""
    keyword = keyword.lower()
    hasil = [user for user in data if keyword in user.lower()]
    return hasil


# ============================================================
# MENU SOSIAL — Titik masuk utama untuk fitur anggota 3
# ============================================================

def menu_sosial(daftar_user, current_user):
    """
    Menampilkan menu utama sistem sosial media.
    Menerima daftar_user (list) dan current_user (string) dari main.py.
    """
    from follow_graph import follow_user, unfollow_user, show_following, show_followers
    from chat_system import send_message, show_chat

    while True:
        print("\n" + "=" * 30)
        print("      MENU SOSIAL MEDIA")
        print("=" * 30)
        print(f"  Login sebagai: {current_user}")
        print("-" * 30)
        print("  1. Follow User")
        print("  2. Lihat Following")
        print("  3. Lihat Followers")
        print("  4. Kirim Chat")
        print("  5. Lihat Chat")
        print("  6. Sorting User (A-Z / Z-A)")
        print("  7. Cari User")
        print("  0. Keluar")
        print("=" * 30)

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            # --- Follow User ---
            target = input("Masukkan username yang ingin di-follow: ").strip()
            follow_user(current_user, target)

        elif pilihan == "2":
            # --- Lihat Following ---
            show_following(current_user)

        elif pilihan == "3":
            # --- Lihat Followers ---
            show_followers(current_user)

        elif pilihan == "4":
            # --- Kirim Chat ---
            penerima = input("Kirim pesan ke (username): ").strip()
            pesan = input("Isi pesan: ").strip()
            send_message(current_user, penerima, pesan)

        elif pilihan == "5":
            # --- Lihat Chat ---
            show_chat(current_user)

        elif pilihan == "6":
            # --- Sorting User ---
            print("\n  Urutkan berdasarkan:")
            print("  1. A-Z (Ascending)")
            print("  2. Z-A (Descending)")
            sub = input("  Pilihan: ").strip()

            if sub == "1":
                hasil = sort_ascending(daftar_user)
                print("\n📋 Daftar User (A-Z):")
            elif sub == "2":
                hasil = sort_descending(daftar_user)
                print("\n📋 Daftar User (Z-A):")
            else:
                print("❌ Pilihan tidak valid.")
                continue

            for i, u in enumerate(hasil, 1):
                print(f"  {i}. {u}")

        elif pilihan == "7":
            # --- Cari User ---
            keyword = input("Masukkan keyword pencarian: ").strip()
            hasil = search_user(daftar_user, keyword)

            print(f"\n🔍 Hasil pencarian '{keyword}':")
            if hasil:
                for i, u in enumerate(hasil, 1):
                    print(f"  {i}. {u}")
            else:
                print("  (tidak ditemukan)")

        elif pilihan == "0":
            print("👋 Keluar dari menu sosial.")
            break

        else:
            print("❌ Pilihan tidak valid, coba lagi.")