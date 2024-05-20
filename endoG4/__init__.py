from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# config database
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object('endoG4.config')

import endoG4.db
import endoG4.routing