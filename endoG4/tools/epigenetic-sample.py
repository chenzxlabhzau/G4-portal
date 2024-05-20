import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4

filepath = "/home/shimw/epigenetic_samples.sort.txt"
with open(filepath, "r") as reader:
    header = ["Sample_id", "Group", "Under_seq", "Quality_rating","sample_name", "ANATOMY", "TYPE","AGE", "SEX"]
    for line in reader:
        fields = line.rstrip("\n").split("\t")
        record = dict(zip(header, fields))
        print(record["Sample_id"])
        if record["Sample_id"].startswith("E"):
            for k in record.copy():
                record[k] = record[k].replace('"', "")
            for k in record.copy():
                if k in ["Under_seq", "Quality_rating"]:
                    record[k] = int(record[k])
            db.epigenetic_sample.insert_one(record)



