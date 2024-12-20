from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin  

from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemySessionUserDatastore
from flask_security import Security

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *



if __name__ == '__main__':
    app.run(debug=True)

admin = Admin(app)


admin.add_view(ModelView(Post, db.session))

#security

