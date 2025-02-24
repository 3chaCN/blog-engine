from backend import TableCategories
from backend import get_categories
from backend import insert_category

class Category():
    def __init__(self, cat):
        self.id = cat[0]
        self.caption = cat[1]

    def get_id(self):
        return self.id

    def get_caption(self):
        return self.caption
    
    def add_category(self):
        insert_category(self.caption)

def get_all_categories()->list:
    c = []
    for cat in get_categories():
        c.append(Category(cat))
    return c
