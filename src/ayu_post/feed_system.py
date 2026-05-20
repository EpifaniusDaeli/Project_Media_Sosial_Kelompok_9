import os

class NodePost:
    def __init(self, post_id,username, caption, likes=0):
        self.post_id = post_id
        self.username = username
        self.caption = caption
        self.likes = likes
        self.comments = []
        self.next = None

class LinkedListFeed:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def tambah_post(self, post_id, username, caption, likes=0):
        new_node = NodePost(post_id, username, caption, likes)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        return new_node
    
    def tambah_post_awal(self, post_id, username, caption, likes=0):
        new_node = NodePost(post_id, username, caption, likes)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        
        self.size += 1
        return new_node
    
    def semua_posts(self):
        posts = []
        current = self.head
        while current:
            posts.append({
                'post_id': current.post_id,
                'username': current.username,
                'caption': current.caption,
                'likes': current.likes,
                'comments': current.comments
            })
            current = current.next
        return posts
    
    def post_by_id(self, post_id):
        current = self.head
        while current:
            if current.post_id == post_id:
                return current
            current = current.next
        return None
    
    def update_likes(self, post_id, new_likes):
        post = self.find_post_by_id(post_id)
        if post:
            post.likes = new_likes
            return True
        return False
    
    def tambah_comment(self, post_id, comment):
        post = self.post_by_id(post_id)
        if post:
            post.comments.apppend(comment)
            return True
        return False
    
    def tampilkan_feed(self, username, following_set):
        posts = self.semua_posts()

        if not posts:
            print("\nBelum ada postingan")
            return []
        
        tampilkan_posts = []
        print("\n" + "="*50)
        print("FEED POSTINGAN")
        print("="*50)

        for idx, post in enumerate(posts, 1):
            if post['username'] in following_set or post['username'] == username:
                tampilkan_posts.append(post)
                print(f"\n{idx}.  {post['username']}")
                print(f"    {post['caption']}")
                print(f"    {post['likes']} likes")
                print(f"    {len(post['comments'])} komentar")
                print("-"*40)
        
        return tampilkan_posts
    
    def simpan_ke_file(self, namafile):
        with open(namafile, 'w') as f:
            current = self.head
            while current:
                f.write(f"{current.post_id}|{current.username}|{current.caption}|{current.likes}\n")
                current = current.next

    def load_from_file(self, namafile):
        try:
            with open(namafile, 'r') as f:
                for baris in f:
                    data = baris.strip().split('|')
                    if len(data) == 4:
                        self.tambah_post(int(data[0]), data[1], data[2], int(data[3]))
        except FileNotFoundError:
            print("File postingan belum ada, akan dibuat baru")