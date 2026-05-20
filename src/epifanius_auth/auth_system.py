#register
#login
#verifikasi akun
'''1.cek username
2.cek password
3.simpan akun ke file'''

def register():
    print("\n=== REGISTER ===")

    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    with open("data_user.txt", "a") as f:
        f.write(username + "," + password + "\n")

    print("Akun berhasil dibuat")
    
def login():
    
    print("\n=== LOGIN ===")

    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    found = False

    with open("data_user.txt", "r") as f:

        for baris in f:

            data = baris.strip().split(",")

            username_file = data[0]
            password_file = data[1]

            if username == username_file and password == password_file:

                found = True
                username_login = username

                print("Login berhasil")