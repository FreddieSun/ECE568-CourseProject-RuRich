from multiprocessing import Pool, cpu_count

from flask import Flask

# from werkzeug.contrib.fixers import ProxyFix

pool = Pool(cpu_count())


app = Flask(__name__)

# app.wsgi_app = ProxyFix(app.wsgi_app)


app.config.from_pyfile('config.py')

from .views import *
