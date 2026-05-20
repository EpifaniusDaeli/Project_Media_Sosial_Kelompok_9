class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(username='{self.username}')"

    def cek_password(self, password: str) -> bool:
        """Memeriksa apakah password yang diberikan cocok."""
        return self.password == password
