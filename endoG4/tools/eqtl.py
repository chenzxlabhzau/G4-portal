import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4
from Bio import SeqIO
from Bio.Seq import MutableSeq
def get_sequence_from_fasta(fa, chromosome, start, end,snp_position,snp_mutate):
    origin_seq = snp_mutate.split("/")[0]
    mutate_seq = snp_mutate.split("/")[1]
    if mutate_seq == "-":
        mutate_seq = ""
    if origin_seq == "-":
        origin_seq = ""
    # 创建一个序列记录字典
    # 获取染色体序列
    chrom_sequence = fa[chromosome].seq
    # 根据位置获取子序列
    # Python索引从0开始，所以start-1
    sub_sequence = chrom_sequence[start-1:end]
    mutable_sub_sequence = MutableSeq(str(sub_sequence))
    mutable_sub_sequence[snp_position-start:snp_position-start + len(origin_seq)] = mutate_seq
    return str(mutable_sub_sequence)

import pandas as pd
# 读取两个CSV文件
table1 = pd.read_csv("/NAS/yulix/20230804_G4database/result/hg.G4.bed", header=None,sep="\t")
table2 = pd.read_csv("/NAS/yulix/all_G4_data/01.G4_pqs/hg_G4.group.bed", header=None,sep="\t")
# 获取两个表格中的'gid'列的唯一值
gid_values_table1 = set(table1[3].unique())
gid_values_table2 = set(table2[3].unique())
extra_gids = gid_values_table2 - gid_values_table1
result = pd.DataFrame(list(extra_gids))
result.to_csv("~/extra_gids.csv", index=False, header=False)


extra_gids_df = pd.read_csv("~/extra_gids.csv", header=None)
extra_gids_set = set(extra_gids_df[0].tolist())

def gwas_seq():
    filepath = "/home/shimw/project/mengwei_G4/data/SNP/GWAS.hg19.allele.txt"
    fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    w = open("/home/shimw/project/mengwei_G4/data/SNP/gwas_mutate_G4.txt", "w")
    w.write("g_id\trsid\tG4\n")
    with open(filepath, "r") as reader:
        header = ["snp_chr", "snp_position", "chromEnd","rsid","phenotype","chr", "start","end", "g_id", "score", "strand","group", "mutate"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            mutate_G4 = get_sequence_from_fasta(record_dict,record['chr'],int(record['start']),
                                    int(record['end']), int(record['snp_position']), record['mutate'])
            w.write(f"{record['g_id']}\t{record['rsid']}\t{mutate_G4}\n")
    w.close()


def import_gwas():
    filepath = "/home/shimw/project/mengwei_G4/data/SNP/gwas_snp_G4.txt"
    with open(filepath, "r") as reader:
        db.eqtl_gwas.drop()
        header = ["snp_chr", "snp_position", "chromEnd","rsid","phenotype","chr", "start","end", "g_id", "score", "strand","group","allele","new_seq","new_score"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            for k in record:
                if k in ["start", "end", "score","chromStart","new_score"]:
                    record[k] = int(record[k])
            del record["chromEnd"]
            del record["new_seq"]
            record["group"] = record["group"].replace("Group", "Level")
            db.eqtl_gwas.insert_one(record)


def cancer_seq():
    fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    filepath = "/NAS/yulix/all_G4_data/01.G4_pqs/6groups.cis.txt"
    w = open("/home/shimw/project/mengwei_G4/data/SNP/cancer_mutate_G4.txt", "w")
    w.write("g_id\trsid\tG4\n")
    with open(filepath, "r") as reader:
        header = ["snp_chr", "snp_position", "chromEnd","rsid",'phenotype',"mutate","gene",'c','d',"chr", "start","end", "g_id", "score", "strand","group"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            mutate_G4 = get_sequence_from_fasta(record_dict,record['chr'],int(record['start']),
                                    int(record['end']), int(record['snp_position']), record['mutate'])
            w.write(f"{record['g_id']}\t{record['rsid']}\t{mutate_G4}\n")
    w.close()





def import_cancer():
    filepath = "/home/shimw/project/mengwei_G4/data/SNP/cancer_eqtl_G4.txt"
    with open(filepath, "r") as reader:
        db.eqtl_cancer.drop()
        header = ["snp_chr", "snp_position", "chromEnd","rsid",'phenotype',"allele","gene",'c','d',"chr", "start","end", "g_id", "score", "strand","group","new_seq","new_score"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            record["g_id"] = record["g_id"].replace("ID", "HG4")
            for k in record:
                if k in ["start", "end", "score","snp_position"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID","HG4")
            del record["chromEnd"]
            del record["c"]
            del record["d"]
            record["group"] = record["group"].replace("Group", "Level")
            db.eqtl_cancer.insert_one(record)



def gtex_seq():
    fasta_file = "/NAS/yulix/mengwei_G4/data/ref/GRCh37.primary_assembly.genome.fa"
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    filepath = "/home/shimw/project/mengwei_G4/data/SNP/G4.GTEx.txt"
    w = open("/home/shimw/project/mengwei_G4/data/SNP/gtex_mutate_G4.txt", "w")
    w.write("g_id\trsid\tG4\n")
    with open(filepath, "r") as reader:
        header = ["snp_chr", "snp_position", "chromEnd","rsid","gene","mutate",'phenotype',"chr", "start","end", "g_id", "score", "strand","a","group"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            mutate_G4 = get_sequence_from_fasta(record_dict,record['chr'],int(record['start']),
                                    int(record['end']), int(record['snp_position']), record['mutate'])
            w.write(f"{record['g_id']}\t{record['rsid']}\t{mutate_G4}\n")
    w.close()

def import_gtex():
    filepath = "/home/shimw/project/mengwei_G4/data/SNP/gtex_eqtl_G4.txt"
    with open(filepath, "r") as reader:
        db.eqtl_gtex.drop()
        header = ["snp_chr", "snp_position", "chromEnd","rsid",'gene',"allele","phenotype","chr", "start","end", "g_id", "score", "strand","a","group","new_seq","new_score" ]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            if record["g_id"] in extra_gids_set:
                continue
            for k in record:
                if k in ["start", "end", "score","snp_position", "new_score"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID","HG4")
            del record["new_seq"]
            del record["chromEnd"]
            del record["a"]
            record["group"] = record["group"].replace("Group", "Level")
            db.eqtl_gtex.insert_one(record)


### 删除自己样本中的gid

