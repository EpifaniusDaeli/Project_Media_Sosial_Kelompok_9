# ============================================================
# SORTING MENU — Pengurutan dan pencarian daftar user
# Struktur data : List (array)
# Algoritma    : Bubble Sort — O(n²), cocok untuk data kecil
# Fitur     :
#   1. Urutkan user A-Z (ascending)
#   2. Urutkan user Z-A (descending)
#   3. Cari user berdasarkan keyword
# ============================================================


def sort_ascending(data: list) -> list:
    """Mengurutkan daftar username dari A ke Z menggunakan Bubble Sort."""
    arr = data.copy()   # salin agar data asli tidak berubah
    n   = len(arr)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            # Tukar jika elemen kiri lebih besar dari kanan
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def sort_descending(data: list) -> list:
    """Mengurutkan daftar username dari Z ke A menggunakan Bubble Sort."""
    return sort_ascending(data)[::-1]


def search_user(data: list, keyword: str) -> list:
    """Mencari user yang mengandung keyword (tidak peka huruf besar/kecil)."""
    keyword = keyword.lower()
    return [user for user in data if keyword in user.lower()]
