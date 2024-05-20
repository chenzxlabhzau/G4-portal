import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4
from Bio import SeqIO

def import_g4_gene():
    filepath = "/NAS/yulix/all_G4_data/01.G4_pqs/G4_gene.txt"
    with open(filepath, "r") as reader:
        header = ["chr", "start","end", "g_id", "score", "strand", "a","b","c","gene_id","gene_name","d","gene_type", "distance"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            for k in record:
                if k in ["start", "end", "score", "distance"]:
                    record[k] = int(record[k])
            record["g_id"] = record["g_id"].replace("ID","HG4")
            del record["a"]
            del record["b"]
            del record["c"]
            del record["d"]
            if "pseudogene" in record['gene_type']:
                record['gene_type'] = "pseudogene"
            record["gene_id"] = record["gene_id"].split(".")[0]
            db['gene_'+record['chr']].insert_one(record)


def delgene():
    for table in db.list_collection_names():
        # if table.startswith("DHS") or table.startswith("chromHMM_") or table.startswith("H3K27ac_"):
        if table.startswith("gene_"):
            # db[table].drop()
            print(table)


# def import_g4_conservation():
#     # filepath = "/home/yulix/G4_analysis/result/savedata2/conservation_score/G4_conservation_information"
#     filepath = "/NAS/yulix/all_G4_data/01.G4_pqs/conservation_score/conservation_information"
#     db.g4_conservation.drop()
#     with open(filepath, "r") as reader:
#         header = reader.readline()
#         header = ["g_id", "size", "phastCons","group","phyloP"]
#         for line in reader:
#             fields = line.rstrip("\n").split("\t")
#             record = dict(zip(header, fields))
#             for k in record:
#                 if k in ["size"]:
#                     record[k] = int(record[k])
#                 if k in ["phastCons","phyloP"]:
#                     record[k] = float(record[k])
#             record["g_id"] = record["g_id"].replace("ID","HG4")
#             db['g4_conservation'].insert_one(record)

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


# 人类的eG4，需要顺便把
def import_eG4():
    record_dict = SeqIO.to_dict(SeqIO.parse("/NAS/yulix/G4_analysis/data/ref/GRCh37.primary_assembly.genome.fa", "fasta"))
    filepath = "/home/shimw/pqsdata/human/hg.group.sort.bed"
    pqs_file = open("/home/shimw/pqsdata/human/human.sort.pqs_gene.txt", "r")
    phastCons = open(f"/home/shimw/project/mengwei_G4/data/conservation/Human.phastCons", "r")
    phyloP = open(f"/home/shimw/project/mengwei_G4/data/conservation/Human.phyloP", "r")
    with open(filepath, "r") as reader:
        db.eg4.drop()
        db.predicted_Human.drop()
        header = ["chr", "start","end", "g_id", "score", "strand","mmm", "group"]
        pqs_header = ["chr", "start","end","g_id","length","strand","score","nt","nb","nm",
                  "rl1","rl2","rl3","ll1","ll2","ll3","a","b", "c", "d","gene_id","gene_name","gene_type", "distance"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            pqs_line = pqs_file.readline()
            pqs_fields = pqs_line.rstrip("\n").split("\t")
            pqs_record = dict(zip(pqs_header, pqs_fields))
            record["phastCons"] = phastCons.readline().strip().split("\t")[5]
            record["phyloP"] = phyloP.readline().strip().split("\t")[5]
            del record["mmm"]
            if record["g_id"]!=pqs_record["g_id"]:
                print(f'{record["g_id"]} not equal')
                break
            if "pseudogene" in pqs_record['gene_type']:
                record['gene_type'] = "pseudogene"
            record["gene_id"] = record["gene_id"].split(".")[0]
            record["g_id"] = record["g_id"].replace("ID","HG4")
            # gene_record = db['gene_'+record['chr']].find_one({"g_id":record["g_id"]})
            # conservation_record = db['g4_conservation'].find_one({"g_id": record["g_id"]})
            # group_record = db[record['chr']+'_g4_group'].find_one({"g_id": record["g_id"]})
            r = {"g_id":record['g_id'],"chr":record['chr'],"start":int(record['start']),"end":int(record['end']),
                 'strand':record['strand'],'score':int(record['score']),'gene_id':pqs_record['gene_id'],
                 'gene_name':pqs_record['gene_name'],'gene_type':pqs_record['gene_type'],"distance":pqs_record["distance"],
                 'size':pqs_record['length'],'group':record["group"],
                 'phastCons': record['phastCons'],'phyloP': record['phyloP'],
                 "rl1":int(pqs_record['rl1']), "rl2":int(pqs_record['rl2']),
                 "rl3":int(pqs_record['rl3']), "ll1":int(pqs_record['ll1']),
                 "ll2":int(pqs_record['ll2']), "ll3":int(pqs_record['ll3']),
                 "seq" : get_sequence_from_fasta(record_dict, record["chr"], int(record['start']),
                                                         int(record['end']), record["strand"])
            }
            db.predicted_Human.insert_one(r)
            if record["group"]!="Non-eG4":
                db.eg4.insert_one(r)

db.eg4.create_index([("g_id",1)])


def delgene():
    for table in db.list_collection_names():
        # if table.startswith("DHS") or table.startswith("chromHMM_") or table.startswith("H3K27ac_"):
        if table.startswith("gene_"):
            db[table].drop()
            print(table)


# def import_mg4_gene():
#     filepath = "/NAS/yulix/20230804_G4database/result/mouse_G4_gene.txt"
#     with open(filepath, "r") as reader:
#         header = ["chr", "start","end", "g_id", "score", "strand", "a","b","c","gene_id","gene_name","d","gene_type", "distance"]
#         for line in reader:
#             fields = line.rstrip("\n").split("\t")
#             record = dict(zip(header, fields))
#             for k in record:
#                 if k in ["start", "end", "score", "distance"]:
#                     record[k] = int(record[k])
#             record["g_id"] = record["g_id"].replace("id","MG4")
#             del record["a"]
#             del record["b"]
#             del record["c"]
#             del record["d"]
#             if "pseudogene" in record['gene_type']:
#                 record['gene_type'] = "pseudogene"
#             record["gene_id"] = record["gene_id"].split(".")[0]
#             db['gene_'+record['chr']].insert_one(record)



# def import_g4_conservation():
#     # filepath = "/home/yulix/G4_analysis/result/savedata2/conservation_score/G4_conservation_information"
#     db.g4_conservation.drop()
#     filepath = "/NAS/yulix/mengwei_G4/result/mm_G4.conservation_information"
#     with open(filepath, "r") as reader:
#         header = reader.readline()
#         header = ["chr", "start", "end", "g_id","score", "strand","phastCons", "phyloP"]
#         for line in reader:
#             fields = line.rstrip("\n").split("\t")
#             record = dict(zip(header, fields))
#             for k in record:
#                 if k in ["start", "end"]:
#                     record[k] = int(record[k])
#                 if k in ["phastCons","phyloP"]:
#                     record[k] = float(record[k])
#             record["g_id"] = record["g_id"].replace("id","MG4")
#             record_new = {
#                 "g_id":record["g_id"],
#                 "size":(record["end"]-record["start"]),
#                 "phastCons":record["phastCons"],
#                 "phyloP": record["phyloP"]
#             }
#             db['g4_conservation'].insert_one(record_new)

def import_meG4():
    record_dict = SeqIO.to_dict(SeqIO.parse("/home/yulix/G4_analysis/data/ref/M10/GRCm38.primary_assembly.genome.fa", "fasta"))
    eg4_file = open("/home/shimw/pqsdata/mouse/mouse.eG4.sort.bed", "r")
    eg4_set = set()
    for i in eg4_file:
        eg4_set.add(i.strip().split("\t")[3])
    phastCons = open(f"/home/shimw/project/mengwei_G4/data/conservation/Mouse.phastCons", "r")
    phyloP = open(f"/home/shimw/project/mengwei_G4/data/conservation/Mouse.phyloP", "r")
    pqs_file = "/home/shimw/pqsdata/mouse/mouse.sort.pqs_gene.txt"
    with open(pqs_file, "r") as reader:
        db.meg4.drop()
        db.predicted_Mouse.drop()
        header = ["chr", "start", "end", "g_id", "length", "strand", "score", "nt", "nb", "nm",
                      "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "a", "b", "c", "d", "gene_id", "gene_name", "gene_type",
                      "distance"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            record["phastCons"] = phastCons.readline().strip().split("\t")[5]
            record["phyloP"] = phyloP.readline().strip().split("\t")[5]
            if "pseudogene" in pqs_record['gene_type']:
                record['gene_type'] = "pseudogene"
            # record["g_id"] =
            # gene_record = db['gene_'+record['chr']].find_one({"g_id":record["g_id"]})
            # conservation_record = db['g4_conservation'].find_one({"g_id": record["g_id"]})
            # group_record = db[record['chr']+'_g4_group'].find_one({"g_id": record["g_id"]})
            r = {"g_id":record["g_id"].replace("id","MG4"),"chr":record['chr'],"start":int(record['start']),"end":int(record['end']),
                 'strand':record['strand'],'score':int(record['score']),'gene_id':record['gene_id'],
                 'gene_name':record['gene_name'],'gene_type':record['gene_type'],"distance":record["distance"],
                 'size':record['length'],'group':"non-eG4",
                 'phastCons': record['phastCons'],'phyloP': record['phyloP'],
                 "rl1":int(record['rl1']), "rl2":int(record['rl2']),
                 "rl3":int(record['rl3']), "ll1":int(record['ll1']),
                 "ll2":int(record['ll2']), "ll3":int(record['ll3']),
                 "seq" : get_sequence_from_fasta(record_dict, record["chr"], int(record['start']),
                                                         int(record['end']), record["strand"])
            }
            db.predicted_Mouse.insert_one(r)
            if record["g_id"] in eg4_set:
                record["group"] = "Level1"
                db.meg4.insert_one(r)

db.meg4.create_index([("g_id",1)])


# def import_ceg4_gene():
#     filepath = "/home/yulix/G4_analysis/result/savedata2/gallus/galllus_G4_gene.txt"
#     with open(filepath, "r") as reader:
#         header = ["chr", "start","end", "g_id", "score", "strand", "e","a","b","c","gene_id","gene_name","d","gene_type", "distance"]
#         for line in reader:
#             fields = line.rstrip("\n").split("\t")
#             record = dict(zip(header, fields))
#             for k in record:
#                 if k in ["start", "end", "score", "distance"]:
#                     record[k] = int(record[k])
#             record["g_id"] = record["g_id"].replace("g","CG4")
#             del record["a"]
#             del record["b"]
#             del record["c"]
#             del record["d"]
#             del record["e"]
#             if "pseudogene" in record['gene_type']:
#                 record['gene_type'] = "pseudogene"
#             record["gene_id"] = record["gene_id"].split(".")[0]
#             db['gene_'+record['chr']].insert_one(record)


# def import_g4_conservation():
#     # filepath = "/home/yulix/G4_analysis/result/savedata2/conservation_score/G4_conservation_information"
#     db.g4_conservation.drop()
#     filepath = "/NAS/yulix/mengwei_G4/result/gallus_G4.conservation_information"
#     with open(filepath, "r") as reader:
#         header = reader.readline()
#         header = ["chr", "start", "end" ,"g_id", "phastCons", "phyloP"]
#         for line in reader:
#             fields = line.rstrip("\n").split("\t")
#             record = dict(zip(header, fields))
#             for k in record:
#                 if k in ["start", "end"]:
#                     record[k] = int(record[k])
#                 if k in ["phastCons","phyloP"]:
#                     record[k] = float(record[k])
#             record["g_id"] = record["g_id"].replace("g","CG4")
#             record_new = {
#                 "g_id":record["g_id"],
#                 "size":(record["end"]-record["start"]),
#                 "phastCons":record["phastCons"],
#                 "phyloP": record["phyloP"]
#             }
#             db['g4_conservation'].insert_one(record_new)
def import_ceG4():
    record_dict = SeqIO.to_dict(SeqIO.parse("/home/yulix/G4_analysis/data/ref/Gallus_gallus/Gallus_gallus.genome.fa", "fasta"))
    eg4_file = open("/home/yulix/G4_analysis/result/savedata2/gallus/gallus.G4.bed", "r")
    eg4_set = set()
    for i in eg4_file:
        eg4_set.add(i.strip().split("\t")[3])
    phastCons = open(f"/home/shimw/project/mengwei_G4/data/conservation/Chicken.phastCons", "r")
    phyloP = open(f"/home/shimw/project/mengwei_G4/data/conservation/Chicken.phyloP", "r")
    pqs_file = "/home/shimw/project/mengwei_G4/data/pqs/chicken.sort.pqs_gene.txt"
    with open(pqs_file, "r") as reader:
        db.ceg4.drop()
        db.predicted_Chicken.drop()
        header = ["chr", "start", "end", "g_id", "length", "strand", "score", "nt", "nb", "nm",
                      "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "a", "b", "c", "d", "gene_id", "gene_name", "gene_type",
                      "distance"]
        for line in reader:
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            record["phastCons"] = phastCons.readline().strip().split("\t")[5]
            record["phyloP"] = phyloP.readline().strip().split("\t")[5]
            if "pseudogene" in record['gene_type']:
                record['gene_type'] = "pseudogene"
            # record["g_id"] =
            # gene_record = db['gene_'+record['chr']].find_one({"g_id":record["g_id"]})
            # conservation_record = db['g4_conservation'].find_one({"g_id": record["g_id"]})
            # group_record = db[record['chr']+'_g4_group'].find_one({"g_id": record["g_id"]})
            r = {"g_id":record["g_id"].replace("g","CG4"),"chr":record['chr'],"start":int(record['start']),"end":int(record['end']),
                 'strand':record['strand'],'score':int(record['score']),'gene_id':record['gene_id'],
                 'gene_name':record['gene_name'],'gene_type':record['gene_type'],"distance":record["distance"],
                 'size':record['length'],'group':"non-eG4",
                 'phastCons': record['phastCons'],'phyloP': record['phyloP'],
                 "rl1":int(record['rl1']), "rl2":int(record['rl2']),
                 "rl3":int(record['rl3']), "ll1":int(record['ll1']),
                 "ll2":int(record['ll2']), "ll3":int(record['ll3']),
                 "seq" : get_sequence_from_fasta(record_dict, record["chr"].replace("chr", ""),
                                                 int(record['start']),int(record['end']), record["strand"])
            }
            db.predicted_Chicken.insert_one(r)
            if record["g_id"] in eg4_set:
                r['group'] = "Level1"
                r['sample_number'] = 1
                r['detect_samples'] = ["DF-1"]
                db.ceg4.insert_one(r)

