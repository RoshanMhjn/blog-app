import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'my_database.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False             
  SECRET_KEY = 'secretkeyrandom'              