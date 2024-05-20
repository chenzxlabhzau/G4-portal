  
from flask import render_template, send_from_directory
from endoG4 import app

# from endoG4.routes.home import home  #ok
from endoG4.routes.predicted import predicted  # ok
from endoG4.routes.group import group
from endoG4.routes.tf import tf
from endoG4.routes.epigenetics import epigenetics
from endoG4.routes.snp import snp
from endoG4.routes.prediction import prediction
from endoG4.routes.detail import detail
from endoG4.routes.sample import celltype

# routing
# app.register_blueprint(home, url_prefix='/api/home')
app.register_blueprint(predicted, url_prefix="/api/predicted")
app.register_blueprint(group, url_prefix="/api/group")
app.register_blueprint(tf, url_prefix="/api/tf")
app.register_blueprint(epigenetics, url_prefix="/api/epigenetics")
app.register_blueprint(snp, url_prefix="/api/eqtl")
app.register_blueprint(prediction, url_prefix="/api/prediction")
app.register_blueprint(detail, url_prefix='/api/detail')
app.register_blueprint(celltype, url_prefix='/api/celltype')

@app.route("/", methods=["GET","POST","OPTIONS"])
def index():
    # return send_from_directory()
    return render_template("index.html")