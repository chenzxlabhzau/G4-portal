from flask import Blueprint, render_template
from endoG4.db import mongo
import os,csv
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from pymongo.collation import Collation
detail = Blueprint("detail", __name__)
api = Api(detail)

BasicInfo_fields = {
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
    "eqtl_cancer_number": fields.Integer,
    "eqtl_gtex_number": fields.Integer,
    "eqtl_gwas_number": fields.Integer,
    "distance":fields.Integer,
    "sample_number":fields.Integer,
    "rl1": fields.Integer,
    "rl2": fields.Integer,
    "rl3": fields.Integer,
    "ll1": fields.Integer,
    "ll2": fields.Integer,
    "ll3": fields.Integer,
    "seq": fields.String
}
de_samples_fields = {
    "sample": fields.String,
    "cell_line": fields.String,
    "treat": fields.String,
    "type":fields.String,
    "source":fields.String,
    "gse": fields.String,
}
detail_fields = {
"basic":fields.Nested(BasicInfo_fields),"de_samples":fields.List(fields.Nested(de_samples_fields))
}
class BasicInfo(Resource):
    @marshal_with(detail_fields)
    def get(self,g_id):
        if g_id.startswith("HG4"):
            result = mongo.db.eg4.find_one({"g_id": g_id}, {"_id": 0})
        elif g_id.startswith("MG4"):
            result = mongo.db.meg4.find_one({"g_id": g_id}, {"_id": 0})
        elif g_id.startswith("CG4"):
            result = mongo.db.ceg4.find_one({"g_id": g_id}, {"_id": 0})
        ll = list(mongo.db.sample_info.find({"sample":{"$in":result['detect_samples']}}))
        return {"basic":result,"de_samples":ll}
api.add_resource(BasicInfo, "/basic/<string:g_id>")


tf_fields = {
        "tf":fields.String,
        "tg_chr":fields.String,
        "tg_start":fields.Integer,
        "tg_end":fields.Integer,
        "score":fields.Integer,
        "match_seq": fields.String
    }

tf_fields = {
    "tf": fields.Nested(
        {
            "tf": fields.String,
            "tg_chr": fields.String,
            "tg_start": fields.Integer,
            "tg_end": fields.Integer,
            "score": fields.Integer,
            "match_seq": fields.String,
            "KO":fields.String

        }
    ),
    "pathway": fields.Nested(
        {
            "tf": fields.String,
            "pathway_name": fields.String,
            "pathway_id": fields.String,
            "ec": fields.String,
            "KO":fields.String

        }
    )
}

class TFInfo(Resource):
    @marshal_with(tf_fields)
    def get(self, g_id):
        result_tmp = mongo.db.gid_tf.find_one({"g_id": g_id}, {"_id": 0})
        result = []
        TFS = []
        if result_tmp:
            for i in result_tmp["tf"]:
                TFS.append(i['tf'])
                aa = {
                    "tf": i['tf'],
                    "tg_chr": i['tg_chr'],
                    "tg_start": i['tg_start'],
                    "tg_end": i['tg_end'],
                    "score": i['score'],
                    "match_seq": i['match_seq'],
                    "KO": i['KO']
                }
                result.append(aa)

        all_result = {
            "tf":result,
            "pathway": list(mongo.db.pathway.find({"tf":{"$in":TFS}}))
        }
        return all_result
api.add_resource(TFInfo, "/tf/<string:g_id>")


snp_fields = {
    "chrom": fields.String,
    "chromStart": fields.Integer,
    "chromEnd": fields.Integer,
    "rsid": fields.String,
    "phenotype": fields.String,
}


class SNP(Resource):
    @marshal_with(snp_fields)
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument("g_id", type=str)
        parser.add_argument("eqtlType", type=str)
        args = parser.parse_args()
        d = args['eqtlType']
        result = mongo.db[d].find({'g_id':args['g_id']}, {"_id": 0})
        return list(result)
api.add_resource(SNP, "/snp")


hmm_fields = {
        "sample":fields.String,
        "chrom":fields.String,
        "chromStart":fields.Integer,
        "chromEnd":fields.Integer,
        "state": fields.String,
        "overlap":fields.Integer,
        "match_seq": fields.String
    }


class HMMInfo(Resource):
    @marshal_with(hmm_fields)
    def get(self, g_id):
        result = mongo.db.basic_chromHMM.find_one({"g_id": g_id}, {"_id": 0})
        if result:
            return result["chromHMM"]
api.add_resource(HMMInfo, "/hmm/<string:g_id>")


dhs_fields = {
        "sample":fields.String,
        "chrom":fields.String,
        "chromStart":fields.Integer,
        "chromEnd":fields.Integer,
        "peak_score": fields.Integer,
        "signalValue": fields.Float,
    "overlap":fields.Integer,
        "match_seq": fields.String
    }
class DHSInfo(Resource):
    @marshal_with(dhs_fields)
    def get(self, g_id):
        result = mongo.db.basic_DHS.find_one({"g_id": g_id}, {"_id": 0})
        if result:
            return result["DHS"]
api.add_resource(DHSInfo, "/dhs/<string:g_id>")


class EnhancerInfo(Resource):
    @marshal_with(dhs_fields)
    def get(self, g_id):
        result = mongo.db.basic_H3K27ac.find_one({"g_id": g_id}, {"_id": 0})
        if result:
            return result["H3K27ac"]
api.add_resource(EnhancerInfo, "/enhancer/<string:g_id>")


class Enrinchment(Resource):

    def get(self, g_id):
        result = mongo.db.enrichment.find_one({"g_id": g_id}, {"_id": 0})
        return result

api.add_resource(Enrinchment, "/enrichment/<string:g_id>")
