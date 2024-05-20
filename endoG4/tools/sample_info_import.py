import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4

def import_sample():
    filepath = "/NAS/yulix/20230804_G4database/result/sample.list"
    filepath = "/home/shimw/sample.list"
    with open(filepath, "r") as reader:
        header = reader.readline()
        header = ["sample","cell_line", "treat", "type", "source", "gse"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["treat"]=="NA":
                record["treat"] = "no treat"
            db.sample_info.insert_one(record)