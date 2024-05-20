import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4

# 获取sample信息，储存在dict中加速
sample_dict = {}
for record in db.sample_info.find():
    sample_dict[record["sample"]] = record


# 首先导入人类的样本信息
def celltype(table_name):
    for record in db[table_name].find():
        for s in record['detect_samples']:
            r = {
                "g_id":record["g_id"],
                "chr":record["chr"],
                "start": record["start"],
                "end": record["end"],
                "strand": record["strand"],
                "group": record["group"],
                "sample":s,
                "cell_line": sample_dict[s]['cell_line'],
                "treat": sample_dict[s]['treat'],
                "type": sample_dict[s]['type'],
                "source": sample_dict[s]['source'],
                "gse": sample_dict[s]['gse']
            }
            db.cell_type.insert_one(r)

db.cell_type.drop()
celltype("eg4")
celltype("meg4")
celltype("ceg4")