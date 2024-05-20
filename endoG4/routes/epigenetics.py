from flask import Blueprint, render_template
from endoG4.db import mongo
import os,csv
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from pymongo.collation import Collation
epigenetics = Blueprint("epigenetics", __name__)
api = Api(epigenetics)


chromhmm_fields = {
    "result":fields.Nested(
        {
            "g_id": fields.String,
            "chr": fields.String,
            "start": fields.Integer,
            "end": fields.Integer,
            "strand": fields.String,
            "group":fields.String,
            "gene_id": fields.String,
            "gene_name": fields.String,
            "gene_type": fields.String,
            "chrom": fields.String,
            "chromStart": fields.Integer,
            "chromEnd": fields.Integer,
            "state": fields.String,
        }
    ),
    "count":fields.Integer
}
epigenetics_fields = {
    "result":fields.Nested(
        {
            "g_id": fields.String,
            "chr": fields.String,
            "start": fields.Integer,
            "end": fields.Integer,
            "strand": fields.String,
            "group":fields.String,
            "gene_id": fields.String,
            "gene_name": fields.String,
            "gene_type": fields.String,
            "chrom": fields.String,
            "chromStart": fields.Integer,
            "chromEnd": fields.Integer,
            "peak_score": fields.Integer
        }
    ),
    "count":fields.Integer
}
class Chromhmm(Resource):
    @marshal_with(chromhmm_fields)
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
                if args['sortcol'] == "loci":
                    sort_col = [('chr', strand),('start', strand)]
                elif args['sortcol'] == "epi_loci":
                    sort_col = [('chrom', strand),('chromStart', strand)]
                else:
                    sort_col = [(args['sortcol'], strand)]
                result = mongo.db["chromHMM_"+args["sample"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["chromHMM_"+args["sample"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        else:
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"gene_id":{"$regex": args["query"], "$options": "i"}},
                {"gene_name": {"$regex": args["query"], "$options": "i"}}
                ]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                if args['sortcol'] == "loci":
                    sort_col = [('chr', strand),('start', strand)]
                elif args['sortcol'] == "epi_loci":
                    sort_col = [('chrom', strand),('chromStart', strand)]
                else:
                    sort_col = [(args['sortcol'], strand)]

                result = mongo.db["chromHMM_"+args["sample"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["chromHMM_"+args["sample"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()

        return {"result": list(result), "count": count}
api.add_resource(Chromhmm, "/chromhmm")


class DHS(Resource):
    @marshal_with(epigenetics_fields)
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
                if args['sortcol'] == "loci":
                    sort_col = [('chr', strand),('start', strand)]
                elif args['sortcol'] == "epi_loci":
                    sort_col = [('chrom', strand),('chromStart', strand)]
                else:
                    sort_col = [(args['sortcol'], strand)]
                result = mongo.db["DHS_"+args["sample"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["DHS_"+args["sample"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        else:
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"gene_id":{"$regex": args["query"], "$options": "i"}},
                {"gene_name": {"$regex": args["query"], "$options": "i"}}
                ]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                if args['sortcol'] == "loci":
                    sort_col = [('chr', strand),('start', strand)]
                elif args['sortcol'] == "epi_loci":
                    sort_col = [('chrom', strand),('chromStart', strand)]
                else:
                    sort_col = [(args['sortcol'], strand)]
                result = mongo.db["DHS_"+args["sample"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["DHS_"+args["sample"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()
        return {"result": list(result), "count": count}
api.add_resource(DHS, "/dhs")


class enhancer(Resource):
    @marshal_with(epigenetics_fields)
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
                if args['sortcol'] == "loci":
                    sort_col = [('chr', strand),('start', strand)]
                elif args['sortcol'] == "epi_loci":
                    sort_col = [('chrom', strand),('chromStart', strand)]
                else:
                    sort_col = [(args['sortcol'], strand)]
                result = mongo.db["H3K27ac_"+args["sample"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["H3K27ac_"+args["sample"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        else:
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"gene_id":{"$regex": args["query"], "$options": "i"}},
                {"gene_name": {"$regex": args["query"], "$options": "i"}}
                ]
            if args['sort'] != "no" and args['sort'] != "":
                strand = sort_option[args.sort]
                if args['sortcol'] == "loci":
                    sort_col = [('chr', strand),('start', strand)]
                elif args['sortcol'] == "epi_loci":
                    sort_col = [('chrom', strand),('chromStart', strand)]
                else:
                    sort_col = [(args['sortcol'], strand)]
                result = mongo.db["H3K27ac_"+args["sample"]].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
            else:
                result = mongo.db["H3K27ac_"+args["sample"]].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()
        return {"result": list(result), "count": count}
api.add_resource(enhancer, "/h3k27ac")


class Download(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("tabIndex", type=int)
        parser.add_argument("query", type=str)
        parser.add_argument("sample", type=str)
        args = parser.parse_args()
        args["query"] = args["query"].strip()
        filename = args["sample"]
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
            condition = {}
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                filename = filename + "_" + args["query"]
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"gene_id":{"$regex": args["query"], "$options": "i"}},
                {"gene_name": {"$regex": args["query"], "$options": "i"}}
                ]
        if args["tabIndex"] == 0:
            filename = "chromHMM_" + filename
            headers = ["g_id","chr", "start", "end", "strand",
                       "group", "gene_id", "gene_name",
                       "gene_type","chrom","chromStart",
                       "chromEnd","state"]
            trueheader = ["G4 id","Chr", "Start", "End", "Strand",
                       "Confidence level", "Gene", "Symbol",
                       "Gene Type","chrom","chromStart",
                       "chromEnd","state"]
            if os.path.exists(os.path.join(basedir, "../static/download/epigenetics/", filename + ".csv")):
                return filename + ".csv"
            result = mongo.db["chromHMM_" + args["sample"]].find(condition,
                                                                 {"g_id":1,"chr": 1, "start": 1, "end": 1, "strand": 1,
                                                                "group":1, "gene_id": 1, "gene_name": 1,
                                                                "gene_type": 1,"chrom":1,"chromStart": 1,
                                                                  "chromEnd": 1,"state": 1,"_id": 0, "by": 1})
        else:
            hh = "DHS_" if args["tabIndex"]==1 else "H3K27ac_"
            filename = hh + filename
            headers = ["g_id","chr", "start", "end", "strand",
                       "group", "gene_id", "gene_name",
                       "gene_type","chrom","chromStart",
                       "chromEnd","peak_score"]
            trueheader = ["G4 id","Chr", "Start", "End", "Strand",
                       "Confidence level", "Gene", "Symbol",
                       "Gene Type","chrom","chromStart",
                       "chromEnd","Peak score"]
            if os.path.exists(os.path.join(basedir, "../static/download/epigenetics/", filename + ".csv")):
                return filename + ".csv"
            result = mongo.db[hh + args["sample"]].find(condition,
                                                            {"g_id": 1, "chr": 1, "start": 1, "end": 1, "strand": 1,
                                                             "group": 1, "gene_id": 1, "gene_name": 1,
                                                             "gene_type": 1, "chrom": 1, "chromStart": 1,
                                                             "chromEnd": 1, "peak_score": 1, "_id": 0, "by": 1}
                                                            )


        if not os.path.exists(os.path.join(basedir,"../static/download/epigenetics/",filename+".csv")):
            with open(os.path.join(basedir,"../static/download/epigenetics/",filename+".csv"),'w') as outfile:
                # headers = ["chr","start", "end","strand","score","gene_id", "gene_name","gene_type"]
                writer = csv.DictWriter(outfile, fieldnames=headers)
                # trueheader = ["Chr","Start", "End","Strand","Score","Gene", "Symbol","Gene Type"]
                writer.writerow(dict(zip(headers, trueheader)))
                for x in result:
                    writer.writerow(x)
        print(os.path.join(basedir,"../static/download/epigenetics/",filename+".csv"))
        return filename + ".csv"
api.add_resource(Download, "/download")


sample_fields = {
    "result":fields.Nested(
        {
            "Sample_id": fields.String,
            "sample_name": fields.String,
            "Group": fields.String,
            "ANATOMY": fields.String,
            "TYPE": fields.String,
            "AGE": fields.String,
            "SEX":fields.String,
            "Under_seq": fields.Integer,
            "Quality_rating": fields.Integer
        }
    ),
    "count": fields.Integer
}

class sample(Resource):
    @marshal_with(sample_fields)
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
        condition = {}
        if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
            condition["$or"] = [
                {"Sample_id":{"$regex": args["query"], "$options": "i"}},
                {"sample_name": {"$regex": args["query"], "$options": "i"}},
                {"Group": {"$regex": args["query"], "$options": "i"}},
                {"ANATOMY": {"$regex": args["query"], "$options": "i"}},
                {"TYPE": {"$regex": args["query"], "$options": "i"}}
            ]
        if args['sort'] != "":
            strand = sort_option[args.sort]
            sort_col = [(args['sortcol'], strand)]
            result = mongo.db.epigenetic_sample.find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
        else:
            result = mongo.db.epigenetic_sample.find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()
        return {"result": list(result), "count": count}
api.add_resource(sample, "/sample")


class SampleDownload(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str)
        args = parser.parse_args()
        args["query"] = args["query"].strip()
        print(args["query"])
        filename = "sample"
        basedir = os.path.abspath((os.path.dirname(__file__)))
        condition = {}
        if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
            filename = filename+"_"+args["query"]
            condition["$or"] = [
                {"Sample_id":{"$regex": args["query"], "$options": "i"}},
                {"sample_name": {"$regex": args["query"], "$options": "i"}},
                {"Group": {"$regex": args["query"], "$options": "i"}},
                {"ANATOMY": {"$regex": args["query"], "$options": "i"}},
                {"TYPE": {"$regex": args["query"], "$options": "i"}}
            ]
        result = mongo.db.epigenetic_sample.find(condition, {"_id": 0})
        if not os.path.exists(os.path.join(basedir,"../static/download/sample/",filename+".txt")):
            with open(os.path.join(basedir,"../static/download/sample/",filename+".txt"),'w') as outfile:
                headers = ["Sample_id",'sample_name','Group', "ANATOMY",'TYPE','AGE','SEX',"Under_seq","Quality_rating"];
                writer = csv.DictWriter(outfile, fieldnames=headers, delimiter='\t')
                trueheader = ["EID","Standardized name", "Group","Anatomy","Type","Age", "Sex","Under seq", "Quality rating"]
                writer.writerow(dict(zip(headers, trueheader)))
                for x in result:
                    writer.writerow(x)
        print(os.path.join(basedir,"../static/download/sample/",filename+".txt"))
        return filename + ".txt"
api.add_resource(SampleDownload, "/sample_donwload")


class SampleInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("eid", type=str)
        args = parser.parse_args()
        args["eid"] = args["eid"].strip()
        result = mongo.db.epigenetic_sample.find_one({"Sample_id": args["eid"]}, {"_id": 0})
        return result
api.add_resource(SampleInfo, "/findSample")