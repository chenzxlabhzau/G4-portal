from flask_pymongo import PyMongo
from endoG4 import app

app.config["MONGO_URI"] = "mongodb://endoG4_reader:endoG4_reader_access@localhost:27017/endoG4"
mongo = PyMongo(app)