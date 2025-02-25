from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from flask import redirect

from datetime import datetime

#import backend
from backend import get_category
from backend import check_password
from posts import Post
from posts import get_last_posts
from posts import get_post_no
from category import Category
from category import get_all_categories
import about

LIST_SIZE=10
#posts = get_last_posts(LIST_SIZE)
#cats = get_all_categories()
app = Flask(__name__)
app.secret_key = b'8ff8aeb6c5b82390529df563b5040c226f13cb336f973d1f52cea48c38f0ce7e' 

#topmenu = ["index", "about"]
#navitm = {"index" : ["item 1", "item 2", "item 3"], "about":["item 1"]}
#url_for('static', filename='style.css')

logged_user = "zyx"

menu = [{"caption":"index","href":"http://127.0.0.1:5000/"},{"caption":"login","href":"/login"},{"caption":"about","href":"/about"}]
menu_admin = [{"caption":"index","href":"http://127.0.0.1:5000/"},{"caption":"write", "href":"/write"},{"caption":"logout","href":"/logout"},{"caption":"about","href":"/about"}]

f = {"author":"Woo"}

topmenu = [menu]
index = 0
app.config.from_pyfile('config.cfg')

@app.route('/')
def index_page():
    posts=get_last_posts(LIST_SIZE)
    cats=get_all_categories()
    if 'username' in session:
        return render_template("posts_adm.html", menubar=menu_admin, categories=cats, content=posts, footer=f)
    else:
        return render_template("posts.html", menubar=menu, categories=cats, content=posts, footer=f)

@app.route('/posts/<int:index>')
def post_page(index):
    cats=get_all_categories()
    if 'username' in session:
        return render_template("post.html", menubar=menu_admin, categories=cats, content=get_post_no(index), footer=f)
    else:
        return render_template("post.html", menubar=menu, categories=cats, content=get_post_no(index), footer=f)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        print("Login attempt with {}".format(request.form['login']))
        if check_password(request.form['login'], request.form['password']) is True:
            session['username'] = request.form['login']
            return redirect(url_for('index_page'))
    return render_template("login.html", menubar=menu, footer=f)

@app.route('/logout')
def logout_page():
    session.pop('username', None)
    return redirect(url_for('index_page'))

@app.route('/about')
def about_page():
    return render_template("about.html", menubar=menu, content=about.c, footer=f)

@app.route('/write', methods=['POST', 'GET'])
def write_page():
    if 'username' in session:
        if request.method == 'POST':
            print(request.form['title'])
            print(request.form['category'])
            print(request.form['data'])
            """ insert_post(request.form['title'],
                            request.form['data'],
                            logged_user,
                            request.form['category'])
            """
            
            # test if category exists. If not, create it before the post
            try:
                c = Category(get_category(request.form['category']))
            except:
                c = Category(["-1", request.form['category']])
                c.add_category()

            p = Post(["-1",
                      request.form['title'],
                      request.form['data'],
                      logged_user,
                      datetime.now().strftime("%Y-%m-%d %H:%M"),
                      request.form['category']
                      ])
            p.add_post()
        return render_template("edit.html", menubar=menu_admin, footer=f)
    else:
        return redirect(url_for('index_page'))
#@app.route('/remove/<int:index>')
#def remove_post():

#@app.route('/submit', methods=['POST'])
#    title = request.form("title")
#    data = request.form("data")
#    category = request.form("category")
    #author = request.form("user")
#    author = logged_user

#def post_article():
#    print(

# define Pager(navbar["lorem", "ipsum"], "title", data[""])
#
# WebPager start from a template "index.html" (html=)
# Next searching for a child named "pname"
# Child page must have {% block body %}{% endblock %} tag
# 

# /status
# /config
# /about (running version, ...)

# /config/[vm1, vm2, ...]
