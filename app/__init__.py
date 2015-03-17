from flask import Flask
import os
from pymongo import Connection, MongoClient
from config import mongoDB_ip, mongoDB_pass, mongoDB_user, mongoDB_port, mongoDB_collection, mongoDB_usersDB
from flask.ext.login import LoginManager
# from flask.ext.openid import OpenID
from config import basedir, SECRET_KEY

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
# lm.user_loader(load_user)
lm.login_view = 'login'
# oid = OpenID(app, os.path.join(basedir, 'tmp'))
app.config["SECRET_KEY"] = SECRET_KEY

uri = "mongodb://" + mongoDB_user + ":" + mongoDB_pass + mongoDB_ip + ':' + str(mongoDB_port)
client = MongoClient(mongoDB_ip + ':' + str(mongoDB_port))
client.admin.authenticate(mongoDB_user, mongoDB_pass)
db = client.stepic

def mongo_db_connection():
    return db[mongoDB_collection]

def mongo_db_userData():
    return db[mongoDB_usersDB]

mongo_db_users = mongo_db_userData()
mongo_db_collection = mongo_db_connection()

def register_blueprints(app):
    # Prevents circular imports
    from app.views import stats
    app.register_blueprint(stats)

register_blueprints(app)

mongo_db_collection = mongo_db_connection()

if __name__ == "__main__":
    app.run()