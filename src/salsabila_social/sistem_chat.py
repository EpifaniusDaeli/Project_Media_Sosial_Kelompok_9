import os

# Path file penyimpanan pesan
DATA_FILE = "data/messages.txt"

# ============================================================
# STRUKTUR DATA: List of dict
# messages = [
#   {"dari": "andi", "ke": "budi", "pesan": "halo"},
#   {"dari": "budi", "ke": "andi", "pesan": "hai juga"}
# ]
# ============================================================

def load_messages():
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
                    "dari": parts[0],
                    "ke": parts[1],
                    "pesan": parts[2]
                })
    return messages


def save_messages(messages):
    """Menyimpan seluruh list pesan ke file data/messages.txt."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        for msg in messages:
            # Format: pengirim|penerima|isi pesan
            f.write(f"{msg['dari']}|{msg['ke']}|{msg['pesan']}\n")


def send_message(pengirim, penerima, pesan):
    """Mengirim pesan dari pengirim ke penerima, lalu menyimpannya ke file."""
    if not pesan.strip():
        print("❌ Pesan tidak boleh kosong.")
        return

    messages = load_messages()

    # Tambahkan pesan baru ke list (seperti enqueue di Queue)
    messages.append({
        "dari": pengirim,
        "ke": penerima,
        "pesan": pesan.strip()
    })

    save_messages(messages)
    print(f"✅ Pesan terkirim ke {penerima}.")


def show_chat(username):
    """Menampilkan semua pesan yang melibatkan username (sebagai pengirim atau penerima)."""
    messages = load_messages()

    # Filter pesan yang berhubungan dengan user ini
    chat_list = [m for m in messages if m["dari"] == username or m["ke"] == username]

    print(f"\n💬 Riwayat chat {username}:")
    if chat_list:
        print("-" * 35)
        for msg in chat_list:
            arah = "→" if msg["dari"] == username else "←"
            lawan = msg["ke"] if msg["dari"] == username else msg["dari"]
            print(f"  [{msg['dari']}] {arah} [{lawan}] : {msg['pesan']}")
        print("-" * 35)
    else:
        print("  (belum ada pesan)")