from backend import get_posts
from backend import get_post_num
from backend import get_author
from backend import get_category
from backend import insert_post 
from backend import update_post
from backend import delete_post

class Post():
    def __init__(self, args=None):
        self.id = args[0]
        self.title = args[1]
        self.content = args[2]
        self.author = args[3]
        self.date = args[4]
        self.category = args[5]

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def get_author(self):
        return self.author

    def get_date(self):
        return str(self.date).split('.')[0]

    def get_category(self):
        return self.category

    def add_post(self):
        """p = TablePosts(title=self.title, 
                       category_id=get_category_id(self.category),
                       author=get_author_id(self.author),
                       date=self.date)"""
        insert_post(self.title, 
                    self.content, 
                    self.author, 
                    self.category, 
                    self.date)
    def modify_post(self):
        update_post(self.id,
                    self.title,
                    self.content, 
                    self.author, 
                    self.category)

    def remove_post(self):
        delete_post(self.id) 

def get_last_posts(count):
    posts = []
    for p in get_posts(count):
        posts.append(Post(p))
    return posts

def get_post_no(id):
    return Post(get_post_num(id))
