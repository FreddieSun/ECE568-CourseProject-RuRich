import os
from multiprocessing import Pool, cpu_count

from flask import Flask
# from werkzeug.contrib.fixers import ProxyFix
from pymongo import MongoClient

pool = Pool(cpu_count())


app = Flask(__name__)

# app.wsgi_app = ProxyFix(app.wsgi_app)


# app.config.from_pyfile('config.py')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

if os.getenv('MONGODB_USERNAME', False):
    app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME', False)
else:
    raise EnvironmentError()

if os.getenv('MONGODB_PASSWORD', False):
    app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD', False)
else:
    raise EnvironmentError()

if os.getenv('MONGODB_HOST', False):
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', False)
else:
    raise EnvironmentError()

app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT', 27017)

url = 'mongodb://{username}:{password}@{host}:{port}'.format(
    username=app.config.get('MONGODB_USERNAME'),
    password=app.config.get('MONGODB_PASSWORD'),
    host=app.config.get('MONGODB_HOST'),
    port=app.config.get('MONGODB_PORT')
)

client = MongoClient(url)
daily = client['ece568']['daily']
realtime = client['ece568']['realtime']
comment = client['ece568']['comment']

from .views import *
from .view_emergency import *
