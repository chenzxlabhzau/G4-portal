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
                if k in ["start", "end", "score","chromStart", "chromEnd"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            record["state"] = record["state"].split("_")[1]
            dbname = "chromHMM_" + record['sample']
            gene_record = db['gene_'+record['chr']].find_one({"g_id": record["g_id"]})
            record["gene_id"] = gene_record['gene_id']
            record["gene_name"] = gene_record['gene_name']
            record["gene_type"] = gene_record['gene_type']
            del record['sample']
            db[dbname].insert_one(record)