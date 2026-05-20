while True:

    print("\n==== MENU ====")
    print("1. Login")
    print("2. Register")
    print("3. Keluar")

    pilihan = input("Pilihan menu: ")

    # ================= LOGIN =================
    from src.epifanius_auth.auth_system import login, register

    if pilihan == "1":

        print("\n=== LOGIN ===")

        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

        found = False

        with open("data/users.txt", "r") as f:

            for baris in f:

                data = baris.strip().split(",")

                username_file = data[0]
                password_file = data[1]

                if username == username_file and password == password_file:

                    found = True
                    username_login = username

                    print("Login berhasil")

                    # ========= MENU USER =========
                    while True:

                        print("\n==== MENU USER ====")
                        print("1. Buat Post")
                        print("2. Lihat Feed")
                        print("3. Follow User")
                        print("4. Logout")

                        pilihan_user = input("Masukkan pilihan: ")

                        # ======== BUAT POST ========
                        if pilihan_user == "1":

                            caption = input("Masukkan caption: ")

                            like = 0

                            with open("data/postingan.txt", "a") as f:
                                f.write(f"{username_login}|{caption}|{like}\n")

                            print("Posting berhasil dibuat")

                        # ======== LIHAT FEED ========
                        elif pilihan_user == "2":

                            following = []

                            with open("data/follow.txt", "r") as f:

                                for baris in f:

                                    data = baris.strip().split("|")

                                    follower = data[0]
                                    target = data[1]

                                    if follower == username_login:
                                        following.append(target)

                            posts = []

                            print("\n=== FEED POSTINGAN ===")

                            with open("data/postingan.txt", "r") as f:

                                nomor = 1

                                for baris in f:

                                    data = baris.strip().split("|")

                                    username_post = data[0]
                                    caption = data[1]
                                    like = data[2]

                                    if username_post in following or username_post == username_login:

                                        posts.append(data)

                                        print("=" * 30)
                                        print(f"{nomor}. Username : {username_post}")
                                        print(f"   Caption  : {caption}")
                                        print(f"   Like     : {like}")
                                        print("=" * 30)

                                        nomor += 1

                            if len(posts) > 0:

                                pilih = int(input("\nLike posting nomor: "))

                                posts[pilih - 1][2] = str(
                                    int(posts[pilih - 1][2]) + 1
                                )

                                semua_post = []

                                with open("data/postingan.txt", "r") as f:

                                    for baris in f:

                                        data = baris.strip().split("|")
                                        semua_post.append(data)

                                count_feed = 0

                                for i in range(len(semua_post)):

                                    username_post = semua_post[i][0]

                                    if username_post in following or username_post == username_login:

                                        if count_feed == pilih - 1:

                                            semua_post[i][2] = posts[pilih - 1][2]

                                        count_feed += 1

                                with open("data/postingan.txt", "w") as f:

                                    for post in semua_post:

                                        f.write(
                                            f"{post[0]}|{post[1]}|{post[2]}\n"
                                        )

                                print("Like berhasil ditambahkan")

                            else:
                                print("Belum ada postingan")

                        # ======== FOLLOW USER ========
                        elif pilihan_user == "3":

                            target = input(
                                "Masukkan username yang ingin di-follow: "
                            )

                            with open("data/follow.txt", "a") as f:
                                f.write(f"{username_login}|{target}\n")

                            print("Berhasil follow user")

                        # ======== LOGOUT ========
                        elif pilihan_user == "4":

                            print("Logout berhasil")
                            break

                        else:
                            print("Pilihan tidak valid")

                    break

        if found == False:
            print("Username atau password salah")

    # ================= REGISTER =================
    elif pilihan == "2":

        print("\n=== REGISTER ===")

        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

        with open("data/users.txt", "a") as f:
            f.write(username + "," + password + "\n")

        print("Akun berhasil dibuat")

    # ================= KELUAR =================
    elif pilihan == "3":

        print("Program selesai")
        break

    else:
        print("Pilihan tidak valid")