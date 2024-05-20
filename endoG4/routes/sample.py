from flask import Blueprint
from endoG4.db import mongo
from pymongo.collation import Collation
import os,csv
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal

celltype = Blueprint("celltype", __name__)
api = Api(celltype)


g4table_fields = {
    "result":fields.Nested(
        {
            "g_id": fields.String,
            "chr": fields.String,
            "start": fields.Integer,
            "end": fields.Integer,
            "strand": fields.String,
            "score": fields.Integer,
            "group":fields.String,
            "sample": fields.String,
            "cell_line": fields.String,
            "treat": fields.String,
            "type": fields.String,
            "source": fields.String,
            "gse": fields.String
        }
    ),
    "count":fields.Integer
}

class G4table(Resource):
    @marshal_with(g4table_fields)
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument("sample", type=str)
        parser.add_argument("query", type=str)
        parser.add_argument("sortcol", type=str, default="")
        parser.add_argument("sort", type=str,default="")
        parser.add_argument("page", type=int, default=0)
        parser.add_argument("size", type=int, default=10)
        args = parser.parse_args()
        record_skip = args["page"] * args["size"]
        record_limit = args["size"]
        sort_option = {"asc": 1, "desc": -1}
        args["query"] = args["query"].strip()
        print(args["sample"])
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
            if args["sample"]!="" and args["sample"]!="undefined":
                condition["sample"] = args["sample"]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                sort_col = [(args['sortcol'], strand)] if args['sortcol'] != "loci" else [('chr', strand),
                                                                                       ('start', strand)]
                result = mongo.db.cell_type.find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                print(condition)
                result = mongo.db.cell_type.find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        else:
            condition = {}
            if args["sample"]!="" and args["sample"]!="undefined":
                condition["sample"] = args["sample"]
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                    {"sample":{"$regex": args["query"], "$options": "i"}},
                    {"cell_line": {"$regex": args["query"], "$options": "i"}},
                    {"treat": {"$regex": args["query"], "$options": "i"}},
                    {"type": {"$regex": args["query"], "$options": "i"}},
                    {"source": {"$regex": args["query"], "$options": "i"}}
                ]
                print(condition)
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                sort_col = [(args['sortcol'], strand)] if args['sortcol'] != "loci" else [('chr', strand),
                                                                                       ('start', strand)]
                result = mongo.db.cell_type.find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db.cell_type.find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()
        return {"result": list(result), "count": count}
api.add_resource(G4table, "/sample")


class Download(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("sample", type=str)
        parser.add_argument("query", type=str)
        args = parser.parse_args()
        args["query"] = args["query"].strip()
        if args["query"].startswith("chr") and ":" in args["query"]:
            chr_position = args["query"].split(":")[0]
            start_position = int(args["query"].split(":")[1].split("-")[0].replace(',', ''))
            end_position = int(args["query"].split(":")[1].split("-")[1].replace(',', ''))
            condition = {
                "chr": chr_position,
                "$or": [
                    {"start": {"$gte": start_position, "$lte": end_position}},
                    {"end": {"$gte": start_position, "$lte": end_position}},
                    {"$and": [
                        {"start": {"$lt": start_position}},
                        {"end": {"$gt": end_position}}
                    ]}
                ]
            }
            filename = "CellType_" + chr_position + "_" + str(start_position) + "_" + str(end_position)
            if args["sample"]!="" and args["sample"]!="undefined":
                condition["sample"] = args["sample"]
                filename = filename + "_" + args["sample"]
        else:
            condition = {}
            filename = "CellType"
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                    {"sample":{"$regex": args["query"], "$options": "i"}},
                    {"cell_line": {"$regex": args["query"], "$options": "i"}},
                    {"treat": {"$regex": args["query"], "$options": "i"}},
                    {"type": {"$regex": args["query"], "$options": "i"}},
                    {"source": {"$regex": args["query"], "$options": "i"}}
                ]
                print(condition)
                filename = filename + "_" + args["query"]
            if args["sample"] != "" and args["sample"] != "undefined":
                condition["sample"] = args["sample"]
                filename = filename + "_" + args["sample"]
        basedir = os.path.abspath((os.path.dirname(__file__)))
        if os.path.exists(os.path.join(basedir, "../static/download/celltype/", filename + ".csv")):
            return filename + ".csv"
        result = mongo.db.cell_type.find(condition,
                                   {"g_id":1,"chr": 1, "start": 1, "end": 1, "strand": 1,
                                    "group":1,"sample": 1, "cell_line": 1, "treat": 1,
                                    "source":1,"gse":1,"_id": 0, "by": 1})
        if not os.path.exists(os.path.join(basedir,"../static/download/celltype/",filename+".csv")):
            with open(os.path.join(basedir,"../static/download/celltype/",filename+".csv"),'w') as outfile:
                print("begin write")
                headers = ["g_id","chr","start", "end","strand","group",
                           "sample", "cell_line","treat","source","gse"]
                writer = csv.DictWriter(outfile, fieldnames=headers)
                trueheader = ["G4 id","Chr","Start", "End","Strand",
                              "Confidence Level","Sample name", "Cell line","Treat",
                              "Source","GSE"]
                writer.writerow(dict(zip(headers, trueheader)))
                for x in result:
                    writer.writerow(x)
        return filename + ".csv"
api.add_resource(Download, "/download")

sample_fields = {
    "sample": fields.String,
    "cell_line": fields.String,
    "treat": fields.String,
    "type": fields.String,
    "source": fields.String,
    "gse": fields.String
}
class SampleInfo(Resource):
    @marshal_with(sample_fields)
    def get(self):
        result = list(mongo.db.sample_info.find())
        return result
api.add_resource(SampleInfo, "/sample_info")
