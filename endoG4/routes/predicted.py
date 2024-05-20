from flask import Blueprint, render_template
from endoG4.db import mongo
import os, csv
from pymongo.collation import Collation
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal

predicted = Blueprint("predicted", __name__)
api = Api(predicted)

predicted_fields = {
    "result":fields.Nested(
        {
            "g_id": fields.String,
            "chr": fields.String,
            "start": fields.Integer,
            "end": fields.Integer,
            "strand": fields.String,
            "score": fields.Integer,
            "group":fields.String,
            "gene_id": fields.String,
            "gene_name": fields.String,
            "gene_type": fields.String,
            "size": fields.Integer,
            "phastCons": fields.Float,
            "phyloP": fields.Float,
            "sample_number": fields.Integer,
            "rl1": fields.Integer,
            "rl2": fields.Integer,
            "rl3": fields.Integer,
            "ll1": fields.Integer,
            "ll2": fields.Integer,
            "ll3": fields.Integer,
            "seq": fields.String
        }
    ),
    "count":fields.Integer
}


class Predicted(Resource):
    @marshal_with(predicted_fields)
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument("query", type=str)
        parser.add_argument("species", type=str)
        parser.add_argument("sortcol", type=str, default="")
        parser.add_argument("sort", type=str,default="")
        parser.add_argument("page", type=int, default=0)
        parser.add_argument("size", type=int, default=10)
        args = parser.parse_args()
        record_skip = args["page"] * args["size"]
        record_limit = args["size"]
        sort_option = {"asc": 1, "desc": -1}
        print("ok")
        args["query"] = args["query"].strip()
        if args["query"].startswith("chr") and ":" in args["query"]:
            chr_position = args["query"].split(":")[0]
            start_position = int(args["query"].split(":")[1].split("-")[0].replace(',',''))
            end_position = int(args["query"].split(":")[1].split("-")[1].replace(',',''))
            condition = {
                "chr":chr_position,
                "$or": [
                    {"start": {"$gte": start_position, "$lte": end_position}},
                    {"end": {"$gte": start_position, "$lte": end_position}},
                    {"$and": [
                        {"start": {"$lt": start_position}},
                        {"end": {"$gt": end_position}}
                    ]}
                    ]
                }
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                sort_col = [(args['sortcol'],strand)] if args['sortcol'] != "loci" else [('chr',strand),('start',strand)]
                result = mongo.db["predicted_" + args["species"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                print(condition)
                result = mongo.db["predicted_"+args["species"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        else:
            print("gene")
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"gene_id":{"$regex": args["query"], "$options": "i"}},
                {"gene_name": {"$regex": args["query"], "$options": "i"}}
                ]
                print(condition)
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                sort_col = [(args['sortcol'], strand)] if args['sortcol'] != "loci" else [('chr', strand),
                                                                                       ('start', strand)]
                print(sort_col)
                result = mongo.db["predicted_" + args["species"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["predicted_"+args["species"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()
        print(count)
        return {"result": list(result), "count": count}
api.add_resource(Predicted, "")


class Download(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str)
        parser.add_argument("species", type=str)
        args = parser.parse_args()
        print("ok")
        args["query"] = args["query"].strip()
        filename = "predicted_" + args["species"]
        basedir = os.path.abspath((os.path.dirname(__file__)))
        if args["query"].startswith("chr") and ":" in args["query"]:
            chr_position = args["query"].split(":")[0]
            start_position = int(args["query"].split(":")[1].split("-")[0].replace(',',''))
            end_position = int(args["query"].split(":")[1].split("-")[1].replace(',',''))
            filename = filename+"_"+chr_position+"_"+str(start_position)+"_"+str(end_position)
            condition = {
                "chr":chr_position,
                "$or": [
                    {"start": {"$gte": start_position, "$lte": end_position}},
                    {"end": {"$gte": start_position, "$lte": end_position}},
                    {"$and": [
                        {"start": {"$lt": start_position}},
                        {"end": {"$gt": end_position}}
                    ]}
                    ]
                }
        else:
            print("gene")
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                filename = filename + "_" + args["query"]
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"gene_id":{"$regex": args["query"], "$options": "i"}},
                {"gene_name": {"$regex": args["query"], "$options": "i"}}
                ]
                print(condition)
        if os.path.exists(os.path.join(basedir, "../static/download/predicted/", filename + ".csv")):
            return filename + ".csv"
        obtain_key = {"g_id":1,"chr": 1, "start": 1, "end": 1, "strand": 1,
                                    "score": 1, "group":1,"gene_id": 1, "gene_name": 1, "gene_type": 1,
                                    "size":1,"phastCons":1,"phyloP":1,"sample_number":1,
                                    "rl1":1,"rl2":1,"rl3":1,"ll1":1,"ll2":1,"ll3":1,"seq":1,"_id": 0, "by": 1}
        headers = ["g_id", "chr", "start", "end", "strand", "score", "group",
                   "gene_id", "gene_name", "gene_type", "size", "phastCons", "phyloP",
                   "sample_number", "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
                   ]
        trueheader = ["G4 id", "Chr", "Start", "End", "Strand",
                      "Score", "Confidence level", "Gene", "Symbol", "Gene Type",
                      "Size", "phastCons", "phyloP", "cell number", "rl1",
                      "rl2", "rl3", "ll1", "ll2", "ll3", "seq"]
        if args["species"] in ["Chicken","Fruit fly", "C. elegans"]:
            del obtain_key["group"]
            headers = ["g_id", "chr", "start", "end", "strand", "score",
                       "gene_id", "gene_name", "gene_type", "size", "phastCons", "phyloP",
                       "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
                       ]
            trueheader = ["G4 id", "Chr", "Start", "End", "Strand",
                          "Score", "Gene", "Symbol", "Gene Type",
                          "Size", "phastCons", "phyloP", "rl1",
                          "rl2", "rl3", "ll1", "ll2", "ll3", "seq"]
        elif args["species"] in ["Rhesus macaque", "Rat", "Rabbit", "Opossums", "Zebrafish"]:
            del obtain_key["group"]
            del obtain_key["phastCons"]
            del obtain_key["phyloP"]
            headers = ["g_id", "chr", "start", "end", "strand", "score",
                       "gene_id", "gene_name", "gene_type", "size",
                       "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
                       ]
            trueheader = ["G4 id", "Chr", "Start", "End", "Strand",
                          "Score", "Gene", "Symbol", "Gene Type",
                          "Size", "rl1",
                          "rl2", "rl3", "ll1", "ll2", "ll3", "seq"]
        result = mongo.db["predicted_"+args["species"]].find(condition, obtain_key)

        if not os.path.exists(os.path.join(basedir,"../static/download/predicted/",filename+".csv")):
            with open(os.path.join(basedir,"../static/download/predicted/",filename+".csv"),'w') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=headers)
                writer.writerow(dict(zip(headers, trueheader)))
                for x in result:
                    writer.writerow(x)
        return filename + ".csv"
api.add_resource(Download, "/download")
