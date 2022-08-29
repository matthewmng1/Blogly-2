from time import timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):

  __tablename__ = "users"

  def __repr__(self):
    p = self
    return f"<User id = {p.id} first_name = {p.first_name} last_name = {p.last_name} image_url = {p.image_url}>"
 

  id = db.Column(db.Integer, 
                 primary_key=True, 
                 autoincrement=True)

  first_name = db.Column(db.String(25), 
                         nullable=False, 
                         unique=False)

  last_name = db.Column(db.String(25), 
                        nullable=False, 
                        unique=False)

  image_url = db.Column(db.String(), 
                        nullable=False, 
                        unique=True)

  blogs = db.relationship("Blog", backref="user", cascade="all, delete-orphan")


class Blog(db.Model):

  __tablename__ = "blogs"

  def _repr__(self):
    p = self
    return f"<Blog id = {p.id} title = {p.title} content = {p.content} created_at = {p.created_at} blog_post = {p.blog_post}>"

  id = db.Column(db.Integer, 
                 primary_key=True, 
                 autoincrement=True)

  title = db.Column(db.String(50), 
                    nullable=False, 
                    unique=True)

  content = db.Column(db.String(), 
                      nullable=False, 
                      unique=False)

  created_at = db.Column(db.DateTime,
                         nullable=False)

  blog_post = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)