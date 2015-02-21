from flask import Flask
from pymongo import Connection, MongoClient
from config import mongoDB_ip, mongoDB_pass, mongoDB_user, mongoDB_port, mongoDB_collection


app = Flask(__name__)

def mongo_db_connection():
    client = MongoClient()
    connection = Connection(mongoDB_ip, mongoDB_port)
    db = connection.Tetrix_log
    return db[mongoDB_collection]

mongo_db_collection = mongo_db_connection()

def register_blueprints(app):
    # Prevents circular imports
    from app.views import stats
    app.register_blueprint(stats)

register_blueprints(app)

mongo_db_collection = mongo_db_connection()

if __name__ == "__main__":
    app.run()