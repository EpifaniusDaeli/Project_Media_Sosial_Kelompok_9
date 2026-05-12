while True:
    print("\n==== MENU ====")
    print("1. Login")
    print("2. Register")
    print("3. Keluar\n")
    
    pilihan = input("Pilihan menu: ")

    if pilihan == "1":
        print("\n=== LOGIN ===")

        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        
        username_login = username
        
        found = False

        with open("data_user.txt", "r") as f:
            for baris in f:
                
                data = baris.strip().split(",")

                username_file = data[0]
                password_file = data[1]
                
                if username == username_file and password == password_file:
                    found = True
                    
                    print("\n==== MENU USER ====")
                    print("1. Buat post")
                    print("2. Lihat Post")
                    print("3. Logout")
                    
                    pilihan = input("Masukkan pilihan: ")
                    if pilihan == "1":
                        username = input("Masukkan Username: ")
                        caption = input("Masukkan Caption: ")
                        like = 0
                        
                        with open("postingan.txt", "a") as f:
                            f.write(f"{username}|{caption}|{like}\n")
                            
                    elif pilihan == "2":
                        following = []

                        with open("follow.txt", "r") as f:
                            for baris in f:
                                
                                data = baris.strip().split("|")
                                follower = data[0]
                                target = data[1]
                                
                                if follower == username_login:
                                    following.append(target)

                        print("\n=== FEED POSTINGAN ===")
                        posts = []
                        with open("postingan.txt", "r") as f:
                            no = 1
                            for baris in f:
                                data = baris.strip().split("|")
                                username_post = data[0]
                                caption = data[1]
                                like = data[2]
                        
                        nomor = 1
                        if username_post in following:
                            print("="*30)
                            print(f"{nomor}. Username : {username_post}")
                            print(f"   Caption  : {caption}")
                            print(f"   Like     : {like}")
                            print("="*30)
                            nomor += 1
                            
                        pilih = int(input("\nLike posting nomor: "))

                        posts[pilih - 1][2]#ini untuk menuju ke baris like yang berindex pilih -1 karena list itu mulai dari 0 dan [2] adalah kolom like

                        posts[pilih - 1][2] = str(int(posts[pilih - 1][2]) + 1)
                        
                        with open("postingan.txt", "w") as f:
                            for post in posts:
                                f.write(f"{post[0]}|{post[1]}|{post[2]}\n")
                                
                        target = input("Masukkan username yang ingin di follow: ")
                        
                        with open("follow.txt", "a") as f:
                            f.write(f"{username_login}|{target}\n")
                    
        if found == False:
            print("Username atau password salah")
    
    elif pilihan == "2":
        print("\n=== REGISTER ===")

        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

        with open("data_user.txt", "a") as f:
            f.write(username + ","+ password + "\n")

        print("Akun berhasil dibuat")
        
    elif pilihan == "3":
        print("Program Selesai")
        break
    
    else:
        print("Pilihan tidak valid")