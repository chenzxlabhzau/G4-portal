from flask import Blueprint, render_template
from endoG4.db import mongo
import os,csv
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from pymongo.collation import Collation
snp = Blueprint("snp", __name__)
api = Api(snp)

eqtl_fields = {
    "result":fields.Nested(
        {
            "snp_chr": fields.String,
            "snp_position": fields.Integer,
            "rsid": fields.String,
            "allele": fields.String,
            "phenotype": fields.String,
            "gene": fields.String,
            "chr": fields.String,
            "start": fields.Integer,
            "end": fields.Integer,
            "strand": fields.String,
            "g_id": fields.String,
            "score": fields.Integer,
            "group": fields.String,
            "new_score": fields.Integer
        }
    ),
    "count":fields.Integer
}


class eQTL(Resource):
    @marshal_with(eqtl_fields)
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument("query", type=str)
        parser.add_argument("eqtlType", type=str)
        parser.add_argument("sortcol", type=str)
        parser.add_argument("sort", type=str)
        parser.add_argument("page", type=int, default=0)
        parser.add_argument("size", type=int, default=10)
        args = parser.parse_args()
        sort_option = {"asc": 1, "desc": -1}
        #type_option = {"eqtl_cancer":"cancer_eQTL_rsid","eqtl_gwas":"GWAS_eQTL_rsid"}
        record_skip = args["page"] * args["size"]
        record_limit = args["size"]
        condition = {}
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
        else:
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                {"rsid":{"$regex": args["query"], "$options": "i"}},
                {"phenotype": {"$regex": args["query"], "$options": "i"}},
                    {"gene": {"$regex": args["query"], "$options": "i"}},
                ]
                print(condition)
        d = args['eqtlType']
        if args['sort'] != "no" and args['sort'] != "":
            strand = sort_option[args.sort]
            if args['sortcol'] == "loci":
                sort_col = [('chr', strand),('start', strand)]
            elif args['sortcol'] == "cloci":
                sort_col = [('snp_chr', strand), ('snp_position', strand)]
            else:
                sort_col = [(args['sortcol'], strand)]
            result = mongo.db[d].find(condition, {"_id": 0}).sort(sort_col).collation(Collation(locale='en_US', numericOrdering = True)).skip(record_skip).limit(record_limit)
        else:
            result = mongo.db[d].find(condition, {"_id": 0}).skip(record_skip).limit(record_limit)
        count = result.count()
        return {"result":list(result),"count":count}
api.add_resource(eQTL, "")


class Download(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("query", type=str)
        parser.add_argument("tabIndex", type=int)
        args = parser.parse_args()
        condition = {}
        tabindex = ["eqtl_gwas","eqtl_gtex","eqtl_cancer"]
        d = tabindex[args['tabIndex']]
        args["query"] = args["query"].strip()
        filename = tabindex[args['tabIndex']]
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
            filename = filename +chr_position+"_"+str(start_position)+"_"+str(end_position)
        else:
            if args["query"] != "" and args["query"] != "null" and args["query"] != "undefined":
                condition["$or"] = [
                {"rsid":{"$regex": args["query"], "$options": "i"}},
                {"phenotype": {"$regex": args["query"], "$options": "i"}},
                    {"g_id": {"$regex": args["query"], "$options": "i"}},
                    {"gene": {"$regex": args["query"], "$options": "i"}},
                ]
                filename = filename + "_" + args["query"]
        basedir = os.path.abspath((os.path.dirname(__file__)))
        if os.path.exists(os.path.join(basedir, "../static/download/eqtl/", filename + ".csv")):
            return filename + ".csv"
        find_field = {"g_id": 1, "chr": 1, "start": 1, "end": 1, "strand": 1, "group": 1, "score": 1,
         "snp_chr": 1, "snp_position": 1, "rsid": 1, "allele": 1, "phenotype": 1, "gene": 1, "new_score": 1, "_id": 0,
         "by": 1}
        headers = ["g_id", "chr", "start", "end", "strand", "group","score",
                   "snp_chr", "snp_position", "rsid", "allele", "phenotype","gene","new_score"]
        trueheader = ["G4 id", "Chr", "Start", "End", "Strand","Confidence level", "Score",
                      "SNP Chr", "SNP Position", "SNP id", "Allele","Phenotype", "Gene", "mutScore"]
        if args['tabIndex']==0:
            print("eqtl_gwas")
            del find_field['gene']
            print(find_field)
            headers = ["g_id", "chr", "start", "end", "strand", "group", "score",
                       "snp_chr", "snp_position", "rsid", "allele", "phenotype", "new_score"]
            trueheader = ["G4 id", "Chr", "Start", "End", "Strand", "Confidence level", "Score",
                          "SNP Chr", "SNP Position", "SNP id", "Allele", "Phenotype", "mutScore"]
        result = mongo.db[d].find(condition, find_field)

        if not os.path.exists(os.path.join(basedir,"../static/download/eqtl/",filename+".csv")):
            with open(os.path.join(basedir,"../static/download/eqtl/",filename+".csv"),'w') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=headers)
                writer.writerow(dict(zip(headers, trueheader)))
                for x in result:
                    writer.writerow(x)
        return filename + ".csv"
api.add_resource(Download, "/download")