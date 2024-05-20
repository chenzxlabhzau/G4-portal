import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4
from Bio import SeqIO

fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

def get_sequence_from_fasta(fa, chromosome, start, end, strand):
    # 创建一个序列记录字典
    # 获取染色体序列
    chrom_sequence = fa[chromosome].seq
    # 根据位置获取子序列
    # Python索引从0开始，所以start-1
    sub_sequence = chrom_sequence[start-1:end]
    if strand=="-":
        sub_sequence=sub_sequence.reverse_complement()
    return str(sub_sequence)


ko_id = {}
for i in db.pathway.find():
    ko_id[i['tf']] = i['KO']


### remove gid
### 获得被去掉的gid列表
import pandas as pd


#cd /NAS/yulix/20230804_G4database/result/G4-TF
# cat group1 group2 group3 group4 group5 group6 > ~/GroupAll
# sort -k 10 /home/shimw/GroupAll > /home/shimw/GroupAll.sort
# sed -i 's/\//-/g' /home/shimw/GroupAll.sort
### 新的导入
def import_tf_id():
    filepath = "/home/shimw/GroupAll.sort"
    tf = ""
    g4 = []
    m=0
    with open(filepath, "r") as reader:
        header = ["chr", "start", "end", "g_id", "score", "strand", "tg_chr", "tg_start", "tg_end", "tf"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            for k in record:
                if k in ["start", "end", "score", "tg_start", "tg_end"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            over_start = max(record["start"], record["tg_start"])
            over_end = min(record["end"], record["tg_end"])
            if record["tf"]=="T":
                record["tf"]="TBXT"
            nn = {"g_id": record["g_id"],
             "chr": record["chr"],
             "start": record["start"],
             "end": record["end"],
             "strand": record["strand"],
             "tf":record["tf"],
             "tg_chr":record["tg_chr"],
             "tg_start": record["tg_start"],
             "tg_end": record["tg_end"],
             "score": record["score"],
             "match_seq":get_sequence_from_fasta(record_dict, record["chr"], over_start, over_end, record["strand"])
                  }
            if tf==record['tf'] and m<5001:
                m = m + 1
                g4.append(nn)
            else:
                if len(g4)>0:
                    db.tf_id.insert_one({"tf":tf,
                                         "KO": ko_id[tf],
                                         'g4':g4,
                                         "g4count":m})
                m = 1
                g4 = []
                tf = record['tf']
                g4.append(nn)
        db.tf_id.insert_one({"tf": tf,
                             "KO" : ko_id[tf],
                             'g4': g4,
                             "g4count": m})




db.tf_id.create_index([("tf",1)])
db.tf_id.drop()


def import_gid_tf(filepath):
    gid = ""
    m=0
    tf = []
    with open(filepath, "r") as reader:
        header = ["chr", "start", "end", "g_id", "score", "strand", "tg_chr", "tg_start", "tg_end", "tf"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            for k in record:
                if k in ["start", "end", "score", "tg_start", "tg_end"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            over_start = max(record["start"], record["tg_start"])
            over_end = min(record["end"], record["tg_end"])
            if record["tf"]=="T":
                record["tf"]="TBXT"
            gg = {
                "tf":record["tf"],
                "tg_chr": record["tg_chr"],
                "tg_start": record["tg_start"],
                "tg_end": record["tg_end"],
                "score": record["score"],
                "KO": ko_id[record["tf"]],
                "match_seq": get_sequence_from_fasta(record_dict, record["chr"], over_start, over_end, record["strand"])

            }
            if gid==record["g_id"]:
                m = m + 1
                tf.append(gg)
            else:
                if len(tf)>0:
                    db.gid_tf.insert_one({"g_id":gid,
                                          "chr": gchr,
                                          "start": gstart,
                                          "end": gend,
                                          "strand": gstrand,
                                          'tf':tf})
                m = 1
                tf = []
                gid = record['g_id']
                gchr = record["chr"]
                gstart = record["start"]
                gend = record["end"]
                gstrand=record["strand"]
                tf.append(gg)


db.gid_tf.drop()


# sort -V -k 4 /NAS/yulix/20230804_G4database/result/G4-TF/group1 > ~/Group1
# sed -i 's/\//-/g' /home/shimw/Group1
import_gid_tf("/home/shimw/Group1")
import_gid_tf("/home/shimw/Group2")
import_gid_tf("/home/shimw/Group3")
import_gid_tf("/home/shimw/Group4")
import_gid_tf("/home/shimw/Group5")
import_gid_tf("/home/shimw/Group6")
db.gid_tf.create_index([("g_id",1)])