import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4

def import_chromHMM():
    filepath = "/home/yulix/G4_analysis/result/savedata/epigenetics/chromHMM_6groups"
    header = ["chrom", "chromStart", "chromEnd","state","sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            for k in record:
                if k in ["chromStart", "chromEnd"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            record["state"] = record["state"].split("_")[1]
            nn = {"chrom": record["chrom"],
                 "chromStart": record["chromStart"],
                 "chromEnd": record["chromEnd"],
                 "state": record["state"],
                 "sample": record["sample"]}
            gene_record = db.g4_chromHMM.find_one({"g_id": record["g_id"]})
            if gene_record:
                db.g4_chromHMM.update_one({"g_id":record['g_id']},{"$addToSet":{'chromHMM':nn}})
            else:
                r = {"g_id":record['g_id'],
                     'chromHMM':[nn]}
                db.g4_chromHMM.insert_one(r)