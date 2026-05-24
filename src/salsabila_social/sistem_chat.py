# ============================================================
# SISTEM CHAT — Pengiriman pesan antar pengguna
# Struktur data : List of dict (antrian pesan / Queue sederhana)
# Format file  : pengirim|penerima|isi pesan
# Fitur     :
#   1. Kirim pesan ke user lain
#   2. Lihat riwayat chat (semua pesan yang melibatkan user)
# ============================================================

import os

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE  = os.path.join(_BASE_DIR, "data", "messages.txt")

# Struktur data pesan:
# messages = [
#   {"dari": "andi", "ke": "budi", "pesan": "halo"},
#   {"dari": "budi", "ke": "andi", "pesan": "hai juga"}
# ]


def load_messages() -> list:
    """Membaca semua pesan dari file dan mengembalikan list pesan."""
    messages = []
    if not os.path.exists(DATA_FILE):
        return messages

    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: pengirim|penerima|isi pesan
            parts = line.split("|", 2)
            if len(parts) == 3:
                messages.append({
                    "dari" : parts[0],
                    "ke"   : parts[1],
                    "pesan": parts[2]
                })
    return messages


def save_messages(messages: list):
    """Menyimpan seluruh list pesan ke file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        for msg in messages:
            f.write(f"{msg['dari']}|{msg['ke']}|{msg['pesan']}\n")


def send_message(pengirim: str, penerima: str, pesan: str):
    """Mengirim pesan dari pengirim ke penerima, lalu menyimpannya ke file."""
    if not pesan.strip():
        print("  [!] Pesan tidak boleh kosong.")
        return

    messages = load_messages()
    messages.append({
        "dari" : pengirim,
        "ke"   : penerima,
        "pesan": pesan.strip()
    })

    save_messages(messages)
    print(f"  [✓] Pesan terkirim ke {penerima}.")


def show_chat(username: str):
    """Menampilkan semua pesan yang melibatkan username (pengirim atau penerima)."""
    messages  = load_messages()
    chat_list = [m for m in messages if m["dari"] == username or m["ke"] == username]

    print(f"\n  Riwayat chat {username}:")
    print("─" * 44)
    if chat_list:
        for msg in chat_list:
            arah  = "→" if msg["dari"] == username else "←"
            lawan = msg["ke"] if msg["dari"] == username else msg["dari"]
            print(f"  [{msg['dari']}] {arah} [{lawan}] : {msg['pesan']}")
    else:
        print("  (belum ada pesan)")
    print("─" * 44)
