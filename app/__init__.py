from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.mail import Mail
import os
import yaml

app = Flask(__name__)
app.secret_key = 'SUPERSECRET' # you should change this to something equally random
app.config['CONFIG_FILE'] = os.path.abspath('app/config.yaml')
configStr = open(app.config['CONFIG_FILE'], 'r')
app.config['CONFIG'] = yaml.load(configStr)
sqlite_db = os.path.abspath('db/elastatus.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s' % sqlite_db


db = SQLAlchemy(app)
auth = HTTPBasicAuth()
mail = Mail(app)

from app.models import *

@app.before_first_request
def create_db():
    if not os.path.exists(sqlite_db):
        db.create_all()


from views import elastatus as elastatus
from admin import admin as admin
app.register_blueprint(elastatus)
app.register_blueprint(admin, url_prefix='/admin')
