import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4
from Bio import SeqIO


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



def overlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

##在group的导入文件里写了
# def import_g4_gene_chr():
#     for i in db.g4_gene.find():
#         db['gene_'+i['chr']].insert_one({"g_id":i['g_id'],
#                                          'gene_id':i['gene_id'],
#                                          'gene_name':i['gene_name'],
#                                          'gene_type':i['gene_type']})

for table in db.list_collection_names():
    if table.startswith("gene_"):
        db[table].create_index([("g_id",1)])

import pandas as pd
##sort -n -k 15 /home/yulix/G4_analysis/result/savedata2/pqs.intersect.narrowpeak/chromHMM_6groups > /home/shimw/H3K27ac_6groups
extra_gids_df = pd.read_csv("~/extra_gids.csv", header=None)
extra_gids_set = set(extra_gids_df[0].tolist())


def import_chromHMM():
    filepath = "/home/shimw/chromHMM_6groups"
    header = ["chrom", "chromStart", "chromEnd","state","sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        gid = ""
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            for k in record:
                if k in ["start", "end", "score","chromStart", "chromEnd"]:
                    record[k] = int(record[k])
            record["state"] = record["state"].split("_")[1]
            dbname = "chromHMM_" + record['sample']
            if gid==record["g_id"]:
                pass
            else:
                gene_record = db['gene_'+record['chr']].find_one({"g_id": record["g_id"]})
            gid=record["g_id"]
            record["gene_id"] = gene_record['gene_id']
            record["gene_name"] = gene_record['gene_name']
            record["gene_type"] = gene_record['gene_type']
            record["overlap"] = overlap([record["start"],record["end"]],
                                        [record["chromStart"],record["chromEnd"]])
            del record['sample']
            record['group']=record['group'].replace("Group", "Level")
            db[dbname].insert_one(record)

##sort -n -k 15 /home/yulix/G4_analysis/result/savedata2/pqs.intersect.narrowpeak/DHS_6groups > /home/shimw/DHS_6groups
def import_DHS():
    filepath = "/home/shimw/DHS_6groups"
    header = ["chrom", "chromStart", "chromEnd","name",'peak_score','a','signalValue','pValue','qValue','peak',"sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        gid = ""
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            for k in record:
                if k in ["start", "end", "score","chromStart", "chromEnd",'peak_score']:
                    record[k] = int(record[k])
            dbname = "DHS_" + record['sample']
            if gid==record["g_id"]:
                pass
            else:
                gene_record = db['gene_'+record['chr']].find_one({"g_id": record["g_id"]})
            gid=record["g_id"]
            record["gene_id"] = gene_record['gene_id']
            record["gene_name"] = gene_record['gene_name']
            record["gene_type"] = gene_record['gene_type']
            del record['a']
            del record['signalValue']
            del record['pValue']
            del record['qValue']
            del record['peak']
            record["overlap"] = overlap([record["start"],record["end"]],
                                        [record["chromStart"],record["chromEnd"]])
            record['group'] = record['group'].replace("Group", "Level")
            db[dbname].insert_one(record)

##sort -n -k 15 /home/yulix/G4_analysis/result/savedata2/pqs.intersect.narrowpeak/H3K27ac_6groups > /home/shimw/H3K27ac_6groups
def import_H3K27ac():
    filepath = "/home/shimw/H3K27ac_6groups"
    header = ["chrom", "chromStart", "chromEnd","name",'peak_score','a','signalValue','pValue','qValue','peak',"sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        gid = ""
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            for k in record:
                if k in ["start", "end", "score","chromStart", "chromEnd",'peak_score']:
                    record[k] = int(record[k])
            dbname = "H3K27ac_" + record['sample']
            if gid==record["g_id"]:
                pass
            else:
                gene_record = db['gene_'+record['chr']].find_one({"g_id": record["g_id"]})
            gid = record["g_id"]
            record["gene_id"] = gene_record['gene_id']
            record["gene_name"] = gene_record['gene_name']
            record["gene_type"] = gene_record['gene_type']
            del record['a']
            del record['signalValue']
            del record['pValue']
            del record['qValue']
            del record['peak']
            record["overlap"] = overlap([record["start"],record["end"]],
                                        [record["chromStart"],record["chromEnd"]])
            record['group'] = record['group'].replace("Group", "Level")
            db[dbname].insert_one(record)

def deleeqtl():
    for table in db.list_collection_names():
        if table.startswith("DHS") or table.startswith("chromHMM_") or table.startswith("H3K27ac_"):
        # if table.startswith("chromHMM_"):
            db[table].drop()
            print(table)


def count_table():
    a = []
    for table in db.list_collection_names():
        if table.startswith("DHS") or table.startswith("chromHMM_") or table.startswith("H3K27ac_"):
            nn = table.split('_')[1]
            a.append(nn)

def index_table():
    a = []
    for table in db.list_collection_names():
        if table.startswith("gene_"):
            db[table].create_index([("g_id", 1)])
set(a)


def basic_chromHMM():
    fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    db.basic_chromHMM.drop()
    filepath = "/home/shimw/chromHMM_6groups"
    header = ["chrom", "chromStart", "chromEnd","state","sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        gid = ""
        result = []
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            over_start = max(int(record["start"]), int(record["chromStart"]))
            over_end = min(int(record["end"]), int(record["chromEnd"]))
            if gid!=record['g_id']:
                if len(result)>0:
                    db.basic_chromHMM.insert_one({"g_id": i["g_id"],
                                                 "chromHMM": result})
                gid = record['g_id']
                result = []
                i = db.eg4.find_one({"g_id": record['g_id']})
                aaa = {
                    "chrom":record["chrom"],
                    "chromStart": int(record["chromStart"]),
                    "chromEnd": int(record["chromEnd"]),
                    "state": record["state"],
                    "sample": record["sample"],
                    "overlap": overlap([int(record["start"]), int(record["end"])],
                                       [int(record["chromStart"]), int(record["chromEnd"])]),
                    "match_seq":get_sequence_from_fasta(record_dict, record["chr"], over_start, over_end, record["strand"])
                }
                result.append(aaa)
            else:
                aaa = {
                    "chrom":record["chrom"],
                    "chromStart": int(record["chromStart"]),
                    "chromEnd": int(record["chromEnd"]),
                    "state": record["state"],
                    "sample": record["sample"],
                    "overlap": overlap([int(record["start"]), int(record["end"])],
                                       [int(record["chromStart"]), int(record["chromEnd"])]),
                    "match_seq": get_sequence_from_fasta(record_dict, record["chr"], over_start, over_end, record["strand"])
                }
                result.append(aaa)
        db.basic_chromHMM.insert_one({"g_id":i["g_id"],
                                  "chromHMM":result})


def basic_DHS():
    fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    db.basic_DHS.drop()
    filepath = "/home/shimw/DHS_6groups"
    header = ["chrom", "chromStart", "chromEnd","name",'peak_score','a','signalValue','pValue','qValue','peak',"sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        gid=""
        result = []
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            over_start = max(int(record["start"]), int(record["chromStart"]))
            over_end = min(int(record["end"]), int(record["chromEnd"]))
            if gid!=record['g_id']:
                if len(result)>0:
                    db.basic_DHS.insert_one({"g_id": i["g_id"],
                                                 "DHS": result})
                gid = record['g_id']
                result = []
                i = db.eg4.find_one({"g_id":record['g_id'] })
                aaa = {
                    "chrom":record["chrom"],
                    "chromStart": int(record["chromStart"]),
                    "chromEnd": int(record["chromEnd"]),
                    "peak_score": int(record["peak_score"]),
                    "signalValue": float(record["signalValue"]),
                    "sample": record["sample"],
                    "overlap": overlap([int(record["start"]), int(record["end"])],
                                       [int(record["chromStart"]), int(record["chromEnd"])]),
                    "match_seq": get_sequence_from_fasta(record_dict,record["chr"], over_start, over_end, record["strand"])
                }
                result.append(aaa)
            else:
                aaa = {
                    "chrom":record["chrom"],
                    "chromStart": int(record["chromStart"]),
                    "chromEnd": int(record["chromEnd"]),
                    "peak_score": int(record["peak_score"]),
                    "signalValue": float(record["signalValue"]),
                    "sample": record["sample"],
                    "overlap": overlap([int(record["start"]), int(record["end"])],
                                       [int(record["chromStart"]), int(record["chromEnd"])]),
                    "match_seq": get_sequence_from_fasta(record_dict,record["chr"], over_start, over_end, record["strand"])
                }
                result.append(aaa)
        db.basic_DHS.insert_one({"g_id":i["g_id"],
                                  "DHS":result})


def basic_H3K27ac():
    fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    filepath = "/home/shimw/H3K27ac_6groups"
    header = ["chrom", "chromStart", "chromEnd","name",'peak_score','a','signalValue','pValue','qValue','peak',"sample","chr", "start", "end", "g_id", "score", "strand","group"]
    with open(filepath, "r") as reader:
        gid=""
        result = []
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            over_start = max(int(record["start"]), int(record["chromStart"]))
            over_end = min(int(record["end"]), int(record["chromEnd"]))
            if gid!=record['g_id']:
                if len(result)>0:
                    db.basic_H3K27ac.insert_one({"g_id": i["g_id"],
                                                 "H3K27ac": result})
                gid = record['g_id']
                result = []
                i = db.eg4.find_one({"g_id":record['g_id'] })
                aaa = {
                    "chrom":record["chrom"],
                    "chromStart": int(record["chromStart"]),
                    "chromEnd": int(record["chromEnd"]),
                    "peak_score": int(record["peak_score"]),
                    "signalValue": float(record["signalValue"]),
                    "sample": record["sample"],
                    "overlap": overlap([int(record["start"]), int(record["end"])],
                                       [int(record["chromStart"]), int(record["chromEnd"])]),
                    "match_seq": get_sequence_from_fasta(record_dict,record["chr"], over_start, over_end, record["strand"])
                }
                result.append(aaa)
            else:
                aaa = {
                    "chrom":record["chrom"],
                    "chromStart": int(record["chromStart"]),
                    "chromEnd": int(record["chromEnd"]),
                    "peak_score": int(record["peak_score"]),
                    "signalValue": float(record["signalValue"]),
                    "sample": record["sample"],
                    "overlap": overlap([int(record["start"]), int(record["end"])],
                                       [int(record["chromStart"]), int(record["chromEnd"])]),
                    "match_seq": get_sequence_from_fasta(record_dict,record["chr"], over_start, over_end, record["strand"])
                }
                result.append(aaa)
        db.basic_H3K27ac.insert_one({"g_id":i["g_id"],
                                  "H3K27ac":result})