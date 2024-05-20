from flask import Blueprint, render_template
from endoG4.db import mongo
import os, csv
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from werkzeug.datastructures import FileStorage
import uuid

prediction = Blueprint("prediction", __name__)
api = Api(prediction)

class filePredict(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prediction_file', type=FileStorage, location='files')
        parser.add_argument("overlapping", type=str)
        parser.add_argument("max_length", type=int)
        parser.add_argument("min_score", type=int)
        parser.add_argument("max_bulge", type=int)
        parser.add_argument("max_mismatch", type=int)
        parser.add_argument("max_defect", type=int)
        parser.add_argument("min_loop", type=int)
        parser.add_argument("max_loop", type=int)
        parser.add_argument("min_run", type=int)
        parser.add_argument("max_run", type=int)
        args = parser.parse_args()
        basedir = os.path.abspath((os.path.dirname(__file__)))
        uuid_rad = str(uuid.uuid4())
        tmp_file_name = 'tmpfile_%s.fa' % uuid_rad
        a = args["prediction_file"]
        tmp_file_path = os.path.join(basedir, "../static/prediction/upload", tmp_file_name)
        a.save(tmp_file_path)

        cmd = "Rscript %s %s %s %s %s %s %s %s %s %s %s %s" % (
            os.path.join(basedir,"../tools/","prediction_G4.R"),
            tmp_file_path,
            args["overlapping"],
            args["max_length"],
            args["min_score"],
            args["max_bulge"],
            args["max_mismatch"],
            args["max_defect"],
            args["min_loop"],
            args["max_loop"],
            args["min_run"],
            args["max_run"]
        )
        print(cmd)
        os.system(cmd)
        os.remove(tmp_file_path)
        result_file_path = 'tmpfile_%s.txt' % uuid_rad
        tmp_file_path = os.path.join(basedir, "../static/prediction/upload", result_file_path)
        cmd = 'sed -i "1i ## Labudova, D., Hon, J. and Lexa, M. (2020) pqsfinder web: G-quadruplex prediction using optimized pqsfinder algorithm. Bioinformatics, 36, 2584-2586." ' + tmp_file_path
        os.system(cmd)
        cmd = 'sed -i "1i ## Hon, J., Martinek, T., Zendulka, J. and Lexa, M. (2017) pqsfinder: an exhaustive and imperfection-tolerant search tool for potential quadruplex-forming sequences in R. Bioinformatics, 33, 3373-3379." ' + tmp_file_path
        os.system(cmd)
        cmd = 'sed -i "1i # The prediction function is implemented based on pqsfinder and pqsfinder web. If you use EndoQuad prediction function and other related results, please cite below original publications." ' + tmp_file_path
        os.system(cmd)
        print(f'Return result file {result_file_path}')
        return result_file_path
api.add_resource(filePredict, "/upload")


class txtPredict(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('seq_str', type=str)
        parser.add_argument("overlapping", type=str)
        parser.add_argument("max_length", type=int)
        parser.add_argument("min_score", type=int)
        parser.add_argument("max_bulge", type=int)
        parser.add_argument("max_mismatch", type=int)
        parser.add_argument("max_defect", type=int)
        parser.add_argument("min_loop", type=int)
        parser.add_argument("max_loop", type=int)
        parser.add_argument("min_run", type=int)
        parser.add_argument("max_run", type=int)
        args = parser.parse_args()
        print(args['seq_str'])
        args['seq_str']=args['seq_str'].strip("\n")
        basedir = os.path.abspath((os.path.dirname(__file__)))
        uuid_rad = str(uuid.uuid4())
        tmp_file_name = 'tmpfile_%s.fa' % uuid_rad
        # a = args["prediction_file"]
        tmp_file_path = os.path.join(basedir, "../static/prediction/upload", tmp_file_name)
        # a.save(tmp_file_path)
        if not args['seq_str'].startswith(">"):
            args['seq_str'] = ">user_seq\n" + args['seq_str']
        print(args['seq_str'])
        w = open(tmp_file_path,"w")
        w.write(args['seq_str'])
        w.close()
        cmd = "Rscript %s %s %s %s %s %s %s %s %s %s %s %s" % (
            os.path.join(basedir,"../tools/","prediction_G4.R"),
            tmp_file_path,
            args["overlapping"],
            args["max_length"],
            args["min_score"],
            args["max_bulge"],
            args["max_mismatch"],
            args["max_defect"],
            args["min_loop"],
            args["max_loop"],
            args["min_run"],
            args["max_run"]
        )
        print(cmd)
        k = os.system(cmd)
        if k == 0:
            result_file_path = 'tmpfile_%s.txt' % uuid_rad
        else:
            result_file_path = 'no_result.txt'
        os.remove(tmp_file_path)
        tmp_file_path = os.path.join(basedir, "../static/prediction/upload", result_file_path)
        cmd = 'sed -i "1i ## Labudova, D., Hon, J. and Lexa, M. (2020) pqsfinder web: G-quadruplex prediction using optimized pqsfinder algorithm. Bioinformatics, 36, 2584-2586." ' + tmp_file_path
        os.system(cmd)
        cmd = 'sed -i "1i ## Hon, J., Martinek, T., Zendulka, J. and Lexa, M. (2017) pqsfinder: an exhaustive and imperfection-tolerant search tool for potential quadruplex-forming sequences in R. Bioinformatics, 33, 3373-3379." ' + tmp_file_path
        os.system(cmd)
        cmd = 'sed -i "1i # The prediction function is implemented based on pqsfinder and pqsfinder web. If you use EndoQuad prediction function and other related results, please cite below original publications." ' + tmp_file_path
        os.system(cmd)
        return result_file_path
api.add_resource(txtPredict, "/txtsearch")