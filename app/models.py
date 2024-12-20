
from app import db 

from time import time

import re

from flask_security import UserMixin, RoleMixin

from datetime import datetime
from sqlalchemy import event


roles_users = db.Table('roles_users',
  
  db.Column('user_id',
            db.Integer,
            db.ForeignKey('user.id')
            ),
  db.Column('role_id',
            db.Integer,
            db.ForeignKey('role.id')
            ),
) 
def slugify(s):
    pattern = r'[^\w\-]' 
    return re.sub(pattern, '-', s).lower()
  



class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(140))
  slug = db.Column(db.String(140), unique=True)
  body = db.Column(db.Text)
  created = db.Column(db.DateTime, default=datetime.utcnow)
    
  def generate_slug(self):
    if self.title:
      self.slug = slugify(self.title)
    else:
      self.slug = str(int(time()))
  
  def __repr__(self):
    return f'<Post id: {self.id}, title: {self.title}>'

@event.listens_for(Post, 'before_insert')
def before_insert_listener(mapper, connection, target):
    target.generate_slug()
    

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  active = db.Column(db.Boolean)
  roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'), lazy='dynamic')
    
class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)