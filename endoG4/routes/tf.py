from flask import Blueprint, render_template
from endoG4.db import mongo
from pymongo.collation import Collation
import os,csv
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal

tf = Blueprint("tf", __name__)
api = Api(tf)

tf_fields = {
    "result":fields.Nested(
        {
            "g_id": fields.String,
            "chr": fields.String,
            "start": fields.Integer,
            "end": fields.Integer,
            "strand":fields.String,
            "tf":fields.String,
            "tg_chr":fields.String,
            "tg_start":fields.Integer,
            "tg_end":fields.Integer,
            "score":fields.Integer,
            "match_seq": fields.String,
            "KO":fields.String
        }
    ),
    "count":fields.Integer
}


class TF(Resource):
    @marshal_with(tf_fields)
    def get(self):
        parser =  reqparse.RequestParser()
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
        if args["query"]=="" or args["query"] == "null" or args["query"] == "undefined":
            pipeline = [ {'$unwind':'$tf'}
                         ]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                if args['sortcol']=="score" or args['sortcol']=="tf":
                    sort_col = {"tf."+args['sortcol']:strand}
                elif args['sortcol']=="loci":
                    sort_col = {"chr": strand, "start": strand}
                elif args['sortcol']=="tfloci":
                    sort_col = {"tf.tg_chr": strand,"tf.tg_start": strand}
                else:
                    sort_col = {args['sortcol']: strand}
                pipeline.append({"$sort": sort_col})
            pipeline.append({'$skip': record_skip})
            pipeline.append({'$limit': record_limit})
            if args['sort'] != "no" and args['sort'] != "":
                result_tmp = mongo.db.gid_tf.aggregate(pipeline,collation=Collation(locale='en_US', numericOrdering = True))
            else:
                result_tmp = mongo.db.gid_tf.aggregate(pipeline)
            count = 8965481
            result = []

            for i in result_tmp:
                aa = {
                    "g_id": i['g_id'],
                    "chr": i['chr'],
                    "start": i['start'],
                    "end": i['end'],
                    "strand": i['strand'],
                    "tf": i['tf']['tf'],
                    "tg_chr": i['tf']['tg_chr'],
                    "tg_start": i['tf']['tg_start'],
                    "tg_end": i['tf']['tg_end'],
                    "score": i['tf']['score'],
                    "match_seq": i['tf']['match_seq'],
                    "KO": i['tf']['KO']
                }
                result.append(aa)
        elif args["query"].startswith("chr") and ":" in args["query"]:
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
            pipeline = [{'$match': condition},
                        {'$unwind': '$tf'}
                        ]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                if args['sortcol']=="score" or args['sortcol']=="tf":
                    sort_col = {"tf."+args['sortcol']:strand}
                elif args['sortcol']=="loci":
                    sort_col = {"chr": strand, "start": strand}
                elif args['sortcol']=="tfloci":
                    sort_col = {"tf.tg_chr": strand,"tf.tg_start": strand}
                else:
                    sort_col = {args['sortcol']: strand}
                pipeline.append({"$sort": sort_col})
            pipeline.append({'$skip': record_skip})
            pipeline.append({'$limit': record_limit})
            if args['sortcol'] != "no" and args['sortcol'] != "undefined":
                result_tmp = mongo.db.gid_tf.aggregate(pipeline,collation=Collation(locale='en_US', numericOrdering = True))
            else:
                result_tmp = mongo.db.gid_tf.aggregate(pipeline)
            c = mongo.db.gid_tf.aggregate([{'$match': condition},
                                          {'$unwind': '$tf'},
                                          {"$count": "totalCount"}
                                          ])
            count = list(c)[0]['totalCount']
            result = []
            for i in result_tmp:
                aa = {
                    "g_id": i['g_id'],
                    "chr": i['chr'],
                    "start": i['start'],
                    "end": i['end'],
                    "strand": i['strand'],
                    "tf": i['tf']['tf'],
                    "tg_chr": i['tf']['tg_chr'],
                    "tg_start": i['tf']['tg_start'],
                    "tg_end": i['tf']['tg_end'],
                    "score": i['tf']['score'],
                    "match_seq": i['tf']['match_seq'],
                    "KO": i['tf']['KO']
                }
                result.append(aa)
        else:
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["tf"] = {"$regex": args["query"], "$options": "i"}
            pipeline = [{'$match':condition},
                         {'$unwind':'$g4'}
                         ]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                if args['sortcol']=="tf":
                    sort_col = {"tf": strand}
                elif args['sortcol']=="loci":
                    sort_col = {"g4.chr": strand, "g4.start": strand}
                elif args['sortcol']=="tfloci":
                    sort_col = {"g4.tg_chr": strand,"g4.tg_start": strand}
                else:
                    sort_col = {"g4."+args['sortcol']:strand}
                pipeline.append({"$sort": sort_col})
            pipeline.append({'$skip': record_skip})
            pipeline.append({'$limit': record_limit})
            # pipeline.append({"$facet":{
            #                 "paginatedResults": [{ "$skip": record_skip}, { "$limit": record_limit}],
            #                 "totalCount":[{"$count":'count'}]
            #             }})
            ###莫名其妙，这样内存超出
            if args['sort'] != "no" and args['sort'] != "":
                result_tmp = mongo.db.tf_id.aggregate(pipeline,collation=Collation(locale='en_US', numericOrdering = True))
            else:
                result_tmp = mongo.db.tf_id.aggregate(pipeline)
            c = mongo.db.tf_id.aggregate([{'$match': condition},
                                          {'$unwind': '$g4'},
                                          {"$count": "totalCount"}
                                          ])
            count = list(c)[0]['totalCount']
            result = []
            for i in result_tmp:
                aa = {
                    "g_id": i['g4']['g_id'],
                    "chr": i['g4']['chr'],
                    "start": i['g4']['start'],
                    "end": i['g4']['end'],
                    "strand": i['g4']['strand'],
                    "tf": i['tf'],
                    "tg_chr": i['g4']['tg_chr'],
                    "tg_start": i['g4']['tg_start'],
                    "tg_end": i['g4']['tg_end'],
                    "score": i['g4']['score'],
                    "match_seq": i['g4']['match_seq'],
                    "KO":i['KO']
                }
                result.append(aa)
        return {"result": list(result), "count": count}
api.add_resource(TF, "")

class Download(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str)
        args = parser.parse_args()
        args["query"] = args["query"].strip()
        basedir = os.path.abspath((os.path.dirname(__file__)))
        if args["query"]=="" or args["query"] == "null" or args["query"] == "undefined":
            pipeline = [
                        {"$project": {"_id": 0}},
                        {'$unwind':'$tf'}
                         ]
            filename = "TF_ALL"
            if os.path.exists(os.path.join(basedir, "../static/download/TF/", filename + ".csv")):
                return filename + ".csv"
            else:
                result = mongo.db.gid_tf.aggregate(pipeline)
        elif args["query"].startswith("chr") and ":" in args["query"]:
            chr_position = args["query"].split(":")[0]
            start_position = int(args["query"].split(":")[1].split("-")[0].replace(',',''))
            end_position = int(args["query"].split(":")[1].split("-")[1].replace(',',''))
            filename = "TF" + "_" + chr_position + "_" + str(start_position) + "_" + str(end_position)
            if os.path.exists(os.path.join(basedir, "../static/download/TF/", filename + ".csv")):
                return filename + ".csv"
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
            pipeline = [{'$match': condition},
                        {"$project": {"_id": 0,"g4count":0}},
                        {'$unwind': '$tf'}
                        ]
            result = mongo.db.gid_tf.aggregate(pipeline)
        else:
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["tf"] = {"$regex": args["query"], "$options": "i"}
            pipeline = [{'$match': condition},
                        {"$project": {"_id": 0}},
                        {'$unwind': '$g4'}
                        ]
            filename = "TF" + "_" + args["query"]
            if os.path.exists(os.path.join(basedir, "../static/download/TF/", filename + ".csv")):
                return filename + ".csv"
            result_tmp = mongo.db.tf_id.aggregate(pipeline)
            if not os.path.exists(os.path.join(basedir, "../static/download/TF/", filename + ".csv")):
                with open(os.path.join(basedir, "../static/download/TF/", filename + ".csv"), 'w') as outfile:
                    headers = ["g_id","chr","start", "end","strand","tf","tg_chr","tg_start",
                           "tg_end","score","match_seq"
                           ]
                    writer = csv.DictWriter(outfile, fieldnames=headers)
                    trueheader = ["G4 id","Chr","Start", "End","Strand",
                              "TF","TF Chr","TF Start","TF End","Score","Match Seq"]
                    writer.writerow(dict(zip(headers, trueheader)))
                    for i in result_tmp:
                        aa = {
                            "g_id": i['g4']['g_id'],
                            "chr": i['g4']['chr'],
                            "start": i['g4']['start'],
                            "end": i['g4']['end'],
                            "strand": i['g4']['strand'],
                            "tf": i['tf'],
                            "tg_chr": i['g4']['tg_chr'],
                            "tg_start": i['g4']['tg_start'],
                            "tg_end": i['g4']['tg_end'],
                            "score": i['g4']['score'],
                            "match_seq": i['g4']['match_seq'],
                        }
                        writer.writerow(aa)
            return filename + ".csv"
        if not os.path.exists(os.path.join(basedir,"../static/download/TF/",filename+".csv")):
            with open(os.path.join(basedir,"../static/download/TF/",filename+".csv"),'w') as outfile:
                headers = ["g_id","chr","start", "end","strand","tf","tg_chr","tg_start",
                           "tg_end","score","match_seq"
                           ]
                writer = csv.DictWriter(outfile, fieldnames=headers)
                trueheader = ["G4 id","Chr","Start", "End","Strand",
                              "TF","TF Chr","TF Start","TF End","Score","Match Seq"]
                writer.writerow(dict(zip(headers, trueheader)))
                for i in result:
                    aa = {
                        "g_id": i['g_id'],
                        "chr": i['chr'],
                        "start": i['start'],
                        "end": i['end'],
                        "strand": i['strand'],
                        "tf": i['tf']['tf'],
                        "tg_chr": i['tf']['tg_chr'],
                        "tg_start": i['tf']['tg_start'],
                        "tg_end": i['tf']['tg_end'],
                        "score": i['tf']['score'],
                        "match_seq": i['tf']['match_seq']
                    }
                    writer.writerow(aa)
        return filename + ".csv"
api.add_resource(Download, "/download")