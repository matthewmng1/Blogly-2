from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Blog

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db' #must do this data base before the other db below
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ITSASECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
  users = User.query.all()
  return render_template('list.html', users=users)

@app.route('/', methods=['POST'])
def create_user():
  first_name = request.form["first_name"]
  last_name = request.form["last_name"]
  image_url = request.form["image_url"]

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)  
  db.session.add(new_user)
  db.session.commit()
  return redirect(f"/{new_user.id}")

@app.route('/<int:user_id>')
def show_user(user_id):
  """Show details about a single user"""
  user = User.query.get_or_404(user_id)
  return render_template("details.html", user=user)

@app.route('/edit/<int:user_id>')
def edit_page(user_id):
  """Edit user details"""
  user = User.query.get_or_404(user_id)
  return render_template("edit_user.html", user=user)

@app.route('/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
  user = User.query.get_or_404(user_id)

  user.first_name = request.form["edit-first-name"]
  user.last_name = request.form["edit-last-name"]
  user.image_url = request.form["edit-image-url"]

  db.session.add(user)
  db.session.commit()
  
  return redirect(f"/{user.id}")

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
  user = User.query.get_or_404(user_id)

  User.query.filter(User.id == user_id).delete()

  db.session.commit()

  return render_template("confirm-delete.html", user=user)

@app.route('/<int:user_id>/posts/new')
def get_blog(user_id):
  user = User.query.get_or_404(user_id)
  return render_template("blog-post.html", user=user)

@app.route('/<int:user_id>/posts/new', methods=['POST'])
def new_blog(user_id):
  user = User.query.get_or_404(user_id)
  title = request.form["blog-title"]
  content = request.form["blog-content"]

  new_blog = Blog(title=title, content=content, user=user)

  db.session.add(new_blog)
  db.session.commit()
  
  return redirect(f"/posts/new/{new_blog.id}")

@app.route('/posts/new/<int:blog_id>')
def show_blog_post(blog_id):
  """Show blog post """
  blog = Blog.query.get_or_404(blog_id)
  return render_template("blogs.html", blog=blog)

@app.route('/edit/posts/<int:blog_id>')
def edit_blog_page(blog_id):
  """Edit blog post"""
  blog = Blog.query.get_or_404(blog_id)
  return render_template("edit-blog.html", blog=blog)

@app.route('/edit/posts/<int:blog_id>', methods=['POST'])
def edit_blog(blog_id):
  """Edit blog post"""
  blog = Blog.query.get_or_404(blog_id)
  blog.title = request.form['new-title']
  blog.content = request.form['new-content']

  db.session.add(blog)
  db.session.commit()

  return redirect(f"/posts/new/{blog.id}")

@app.route('/delete/<int:blog_id>')
def delete_blog(blog_id):
  blog = Blog.query.get_or_404(blog_id)

  Blog.query.filter(Blog.id == blog_id).delete()

  db.session.commit()

  return render_template("confirm-delete.html", blog=blog)