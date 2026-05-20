import os

# Path file penyimpanan data follow
DATA_FILE = "data/follow.txt"

# ============================================================
# STRUKTUR DATA: Graph menggunakan dictionary
# graph = { "andi": ["budi", "caca"], "budi": ["andi"] }
# ============================================================

def load_follow_data():
    """Membaca data follow dari file dan mengembalikan graph (dictionary)."""
    graph = {}
    if not os.path.exists(DATA_FILE):
        return graph

    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: andi:budi,caca
            parts = line.split(":")
            user = parts[0]
            following = parts[1].split(",") if parts[1] else []
            graph[user] = [x for x in following if x]  # hapus string kosong
    return graph


def save_follow_data(graph):
    """Menyimpan graph follow ke file data/follow.txt."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        for user, following in graph.items():
            # Format: andi:budi,caca
            f.write(f"{user}:{','.join(following)}\n")


def follow_user(username, target):
    """User melakukan follow ke user lain (target)."""
    if username == target:
        print("❌ Tidak bisa follow diri sendiri.")
        return

    graph = load_follow_data()

    # Pastikan kedua user ada di graph
    if username not in graph:
        graph[username] = []
    if target not in graph:
        graph[target] = []

    if target in graph[username]:
        print(f"⚠️  {username} sudah mengikuti {target}.")
    else:
        graph[username].append(target)
        save_follow_data(graph)
        print(f"✅ {username} sekarang mengikuti {target}.")


def unfollow_user(username, target):
    """User berhenti mengikuti (unfollow) user lain."""
    graph = load_follow_data()

    if username not in graph or target not in graph[username]:
        print(f"⚠️  {username} tidak mengikuti {target}.")
    else:
        graph[username].remove(target)
        save_follow_data(graph)
        print(f"✅ {username} berhenti mengikuti {target}.")


def show_following(username):
    """Menampilkan daftar user yang di-follow oleh username."""
    graph = load_follow_data()
    following = graph.get(username, [])

    print(f"\n📋 {username} mengikuti {len(following)} akun:")
    if following:
        for i, user in enumerate(following, 1):
            print(f"  {i}. {user}")
    else:
        print("  (belum mengikuti siapapun)")


def show_followers(username):
    """Menampilkan daftar user yang mengikuti username (followers)."""
    graph = load_follow_data()

    # Cari siapa saja yang punya username di list following mereka
    followers = [user for user, following in graph.items() if username in following]

    print(f"\n👥 {username} diikuti oleh {len(followers)} akun:")
    if followers:
        for i, user in enumerate(followers, 1):
            print(f"  {i}. {user}")
    else:
        print("  (belum ada yang mengikuti)")