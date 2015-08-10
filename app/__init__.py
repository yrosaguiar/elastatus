from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.mail import Mail
from flask.ext.cache import Cache
import os
import yaml

app = Flask(__name__)
app.secret_key = 'SUPERSECRET' # you should change this to something equally random
app.config['CONFIG_FILE'] = os.path.abspath('app/config.yaml')
configStr = open(app.config['CONFIG_FILE'], 'r')
app.config['CONFIG'] = yaml.load(configStr)
sqlite_db = os.path.abspath('db/elastatus.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s' % sqlite_db

# Allow arbitrary python code in Jinja templates
app.jinja_options['extensions'].append('jinja2.ext.do')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
mail = Mail(app)
cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple',
                            'CACHE_DEFAULT_TIMEOUT':app.config['CONFIG']['sgaudit']['cache_timeout']
                            })

if app.config['CONFIG']['jobs']['enabled']:
    from jobs import *


from app.models import *

@app.before_first_request
def create_db():
    if not os.path.exists(sqlite_db):
        db.create_all()


from views import elastatus as elastatus
from api import api as api
from admin import admin as admin
app.register_blueprint(elastatus)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
