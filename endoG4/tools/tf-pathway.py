import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4


import json
import re

with open("/home/shimw/hsa00001.json") as f:
    ko_map_data = json.load(f)

#tfs = db.tf_id.distinct("tf")

tfs=set()
reader = open("/home/shimw/GroupAll.sort", "r")
for line in reader:
    stn = line.rstrip("\n").split("\t")[-1]
    if stn in tfs:
        continue
    tfs.add(stn)
tfs.add("TBXT")

with open("/home/shimw/KEGG_pathway_ko.txt", "w") as oh:
    line = "level1_pathway_id\tlevel1_pathway_name\tlevel2_pathway_id\tlevel2_pathway_name"
    line += "\tlevel3_pathway_id\tlevel3_pathway_name\tko\tko_name\tec\n"
    oh.write(line)
    for level1 in ko_map_data["children"]:
        m = re.match(r"(\S+)\s+([\S\w\s]+)", level1["name"])
        level1_pathway_id = m.groups()[0].strip()
        level1_pathway_name = m.groups()[1].strip()
        for level2 in level1["children"]:
            m = re.match(r"(\S+)\s+([\S\w\s]+)", level2["name"])
            level2_pathway_id = m.groups()[0].strip()
            level2_pathway_name = m.groups()[1].strip()
            for level3 in level2["children"]:
                m = re.match(r"(\S+)\s+([^\[]*)", level3["name"])
                level3_pathway_id = m.groups()[0].strip()
                level3_pathway_name = m.groups()[1].strip()
                if "children" in level3:
                    for ko in level3["children"]:
                        m = re.match(r"(\S+)\s+(\S+);\s+([^\[]+)\s*(\[EC:\S+(?:\s+[^\[\]]+)*\])*", ko["name"])
                        if m is not None:
                            aliname = ko["name"].split("\t")[1].split(";")[0].split(" ")[1]
                            ko_id = m.groups()[0].strip()
                            ko_name = m.groups()[1].strip()
                            ko_des = m.groups()[2].strip()
                            ec = m.groups()[3]
                            if ec==None:
                                ec = "-"
                        if ko_name in tfs:
                            line = level1_pathway_id + "\t" + level1_pathway_name + "\t" + level2_pathway_id + "\t" + level2_pathway_name
                            line += "\t" + level3_pathway_id + "\t" + level3_pathway_name + "\t" + ko_id + "\t" + ko_name + "\t" + ec + "\n"
                            oh.write(line)
                        else:
                            if aliname in tfs:
                                line = level1_pathway_id + "\t" + level1_pathway_name + "\t" + level2_pathway_id + "\t" + level2_pathway_name
                                line += "\t" + level3_pathway_id + "\t" + level3_pathway_name + "\t" + ko_id + "\t" + aliname  + "\t" + ec + "\n"
                                oh.write(line)
                            else:
                                line = level1_pathway_id + "\t" + level1_pathway_name + "\t" + level2_pathway_id + "\t" + level2_pathway_name
                                line += "\t" + level3_pathway_id + "\t" + level3_pathway_name + "\t" + ko_id + "\t" + ko_name + "\t" + ec + "\n"
                                oh.write(line)





with open("/home/shimw/KEGG_pathway_ko.txt", "r") as reader:
    ll=[]
    header = reader.readline().rstrip("\n").split("\t")
    for line in reader:
        fields = line.rstrip("\n").split("\t")
        record = dict(zip(header, fields))
        if record["ko_name"] in tfs:
            result = {
                "tf": record["ko_name"],
                "KO": "hsa:"+record["ko"],
                "pathway_name": record["level3_pathway_name"],
                "pathway_id": "hsa"+record["level3_pathway_id"],
                "ec": fields[-1].strip("[EC:").strip("]")
            }
            bb = db.pathway.find_one({"tf": record["ko_name"],"pathway_name": record["level3_pathway_name"]})
            if bb:
                print(record["ko_name"])
                ll.append(record["ko_name"])
                continue
            db.pathway.insert_one(result)

ff = db.pathway.distinct("tf")
ll = set(ll)
import requests
for id in ll:
    url="https://rest.kegg.jp/find/genes/" + id
    resp = requests.get(url)
    aa = resp.text
    line = aa.split("\n")[0]
    ko = line.split("\t")[0]
    print(id)
    db.pathway.update_many({"tf":id}, {"$set":{"KO":ko}})



kk = []
for i in tfs:
    if i not in ff:
        print(i)
        kk.append(i)


import requests
for id in kk:
    # url="https://rest.kegg.jp/find/genes/" + id
    # resp = requests.get(url)
    # aa = resp.text
    # line = aa.split("\n")[0]
    # ko = line.split("\t")[0]
    # if id=="T":
    #     id = "TBXT"
    result = {
                "tf": id,
                "KO": "",
                "pathway_name": "",
                "pathway_id": "",
                "ec": ""
            }
    print(id)
    db.pathway.insert_one(result)



for id in kk:
    db.pathway.delete_one({"tf":id})