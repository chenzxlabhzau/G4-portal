import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4
from gseapy import enrichr
import math
from scipy.stats import fisher_exact
import numpy as np
from collections import defaultdict
# tf_pathway_dicts_from_mongodb = []

# with open("/home/shimw/KEGG_pathway_ko.txt", "r") as reader:
#     header = reader.readline().rstrip("\n").split("\t")
#     for line in reader:
#         if line.startswith("Not Included in Pathway"):
#             continue
#         fields = line.rstrip("\n").split("\t")
#         record = dict(zip(header, fields))
#         tf_pathway_dicts_from_mongodb.append(
#             {"TF":"hsa:" + record["ko"], "pathway":record["level3_pathway_name"]}
#         )


# All_tf = set(dict_item['TF'] for dict_item in tf_pathway_dicts_from_mongodb)
# pathway_to_tf = defaultdict(set)
# for tf_pathway_dict in tf_pathway_dicts_from_mongodb:
#     if tf_pathway_dict["TF"] not in pathway_to_tf[tf_pathway_dict["pathway"]]:
#         pathway_to_tf[tf_pathway_dict["pathway"]].add(tf_pathway_dict["TF"])


db.gid_tf.find(no_cursor_timeout=True).limit(100000).batch_size(200)
db.gid_tf.find(no_cursor_timeout=True).skip(100000).limit(100000).batch_size(200)
db.gid_tf.find(no_cursor_timeout=True).skip(200000).limit(100000).batch_size(200)
db.gid_tf.find(no_cursor_timeout=True).skip(300000).batch_size(200)
for record in db.gid_tf.find(no_cursor_timeout=True).skip(300000).batch_size(200):
    binded_tf_list = []
    for k in record["tf"]:
        if k["tf"]!="":
            binded_tf_list.append(k["tf"])
    if len(binded_tf_list)<5:
        continue
    try:
        kegg_result = enrichr(gene_list=binded_tf_list, gene_sets='/home/shimw/KEGG_2021_Human.gmt')
    except ValueError:
        kegg_result = None
    try:
        go_result = enrichr(gene_list=binded_tf_list, gene_sets='/home/shimw/GO_Biological_Process_2021.gmt')
    except ValueError:
        go_result = None
    if kegg_result:
        print(f'{record["g_id"]} kegg done')
        kegg_df = kegg_result.results.head(10)
        kegg_df = kegg_df[kegg_df['Adjusted P-value']<1]
        kegg_term = kegg_df['Term'].values.tolist()
        kegg_p = kegg_df['Adjusted P-value'].values.tolist()
        kegg_overlap_num = [int(k.split("/")[0]) for k in kegg_df['Overlap'].values.tolist()]
        kegg_Odds_Ratio = kegg_df['Odds Ratio'].values.tolist()
        kegg = []
        for x,y,z,i in zip(kegg_term,kegg_Odds_Ratio,kegg_overlap_num,kegg_p):
            kegg.append({"pathway":x,"GeneRatio":y,"count":z,"padjust":-math.log10(i)})
    else:
        kegg = []
    if go_result:
        print(f'{record["g_id"]} go done')
        go_df = go_result.results.head(10)
        go_df = go_df[go_df['Adjusted P-value']<1]
        go_p = go_df['Adjusted P-value'].values.tolist()
        go_term = [k.split(" (")[0] for k in go_df['Term'].values.tolist()]
        go_overlap_num = [int(k.split("/")[0]) for k in go_df['Overlap'].values.tolist()]
        go_Odds_Ratio = go_df['Odds Ratio'].values.tolist()
        go = []
        for x,y,z,i in zip(go_term,go_Odds_Ratio,go_overlap_num,go_p):
            go.append({"pathway":x,"GeneRatio":y,"count":z,"padjust":-math.log10(i)})
    else:
        go = []
    db.enrichment.insert_one(
        {"g_id":record["g_id"],
         "total_tf":len(binded_tf_list),
         "kegg":kegg,
         "go":go
         }
    )



for record in db.gid_tf.find({"KO":{"$ne":""}}).batch_size(200):
    binded_tf_list = []
    for k in record["tf"]:
        binded_tf_list.append(k["tf"])
    if len(binded_tf_list)>10:
        break




# 判断gmt的通路是否在之前的kegg通路中
tf_pathway_dicts_from_mongodb = []

with open("/home/shimw/KEGG_pathway_ko.txt", "r") as reader:
    header = reader.readline().rstrip("\n").split("\t")
    for line in reader:
        if line.startswith("Not Included in Pathway"):
            continue
        fields = line.rstrip("\n").split("\t")
        record = dict(zip(header, fields))
        tf_pathway_dicts_from_mongodb.append(
           record["level3_pathway_name"]
        )
tf_pathway_dicts_from_mongodb = set(tf_pathway_dicts_from_mongodb)

kkkkk=[]
with open("/home/shimw/KEGG_2021_Human.gmt", "r") as reader:
    for line in reader:
        if line.startswith("Not Included in Pathway"):
            continue
        fields = line.rstrip("\n").split("\t")
        kkkkk.append(
           fields[0]
        )
kkkkk = set(kkkkk)

for i in kkkkk:
    if i in tf_pathway_dicts_from_mongodb:
        continue
    else:
        print(i)


