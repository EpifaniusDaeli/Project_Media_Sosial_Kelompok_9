# ============================================================
# FOLLOW GRAPH — Graf relasi follow antar pengguna
# Struktur data : Graph (dictionary of lists)
# Format file  : username:following1,following2,...
# Fitur     :
#   1. Follow user lain
#   2. Unfollow user
#   3. Lihat daftar following
#   4. Lihat daftar followers
# ============================================================

import os

# Path absolut agar tidak bergantung pada direktori kerja saat ini
_BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE  = os.path.join(_BASE_DIR, "data", "follow.txt")

# Struktur graf:
# graph = { "andi": ["budi", "caca"], "budi": ["andi"] }


def load_follow_data() -> dict:
    """Membaca data follow dari file dan mengembalikan graph (dictionary)."""
    graph = {}
    if not os.path.exists(DATA_FILE):
        return graph

    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Format: username:following1,following2
            if ":" not in line:
                continue   # lewati baris yang tidak valid

            parts     = line.split(":", 1)
            user      = parts[0]
            following = [x for x in parts[1].split(",") if x]
            graph[user] = following

    return graph


def save_follow_data(graph: dict):
    """Menyimpan graph follow ke file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        for user, following in graph.items():
            f.write(f"{user}:{','.join(following)}\n")


def follow_user(username: str, target: str):
    """User melakukan follow ke user lain."""
    if username == target:
        print("  [!] Tidak bisa follow diri sendiri.")
        return

    graph = load_follow_data()

    if username not in graph:
        graph[username] = []
    if target not in graph:
        graph[target] = []

    if target in graph[username]:
        print(f"  [!] {username} sudah mengikuti {target}.")
    else:
        graph[username].append(target)
        save_follow_data(graph)
        print(f"  [✓] {username} sekarang mengikuti {target}.")


def unfollow_user(username: str, target: str):
    """User berhenti mengikuti user lain."""
    graph = load_follow_data()

    if username not in graph or target not in graph[username]:
        print(f"  [!] {username} tidak mengikuti {target}.")
    else:
        graph[username].remove(target)
        save_follow_data(graph)
        print(f"  [✓] {username} berhenti mengikuti {target}.")


def show_following(username: str):
    """Menampilkan daftar user yang di-follow oleh username."""
    graph     = load_follow_data()
    following = graph.get(username, [])

    print(f"\n  {username} mengikuti {len(following)} akun:")
    if following:
        for i, user in enumerate(following, 1):
            print(f"    {i}. {user}")
    else:
        print("    (belum mengikuti siapapun)")


def show_followers(username: str):
    """Menampilkan daftar user yang mengikuti username (followers)."""
    graph     = load_follow_data()
    followers = [user for user, following in graph.items() if username in following]

    print(f"\n  {username} diikuti oleh {len(followers)} akun:")
    if followers:
        for i, user in enumerate(followers, 1):
            print(f"    {i}. {user}")
    else:
        print("    (belum ada yang mengikuti)")
