import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4

####更新GTEx eQTL 数量



def update_eqtl_number():
    db.eg4.update_many({},
                      {"$set": {"eqtl_cancer_number": 0,
                                "eqtl_gtex_number": 0,
                                "eqtl_gwas_number": 0}})
    for g_id in db.eqtl_gtex.distinct("g_id"):
        tmp_result = db.eqtl_gtex.distinct("rsid", {"g_id":g_id})
        db.eg4.update_one({"g_id":g_id},
                           {"$set": {"eqtl_gtex_number": len(tmp_result)}})
    for g_id in db.eqtl_cancer.distinct("g_id"):
        tmp_result = db.eqtl_cancer.distinct("rsid", {"g_id":g_id})
        db.eg4.update_one({"g_id":g_id},
                           {"$set": {"eqtl_cancer_number": len(tmp_result)}})
    for g_id in db.eqtl_gwas.distinct("g_id"):
        tmp_result = db.eqtl_gwas.distinct("rsid", {"g_id":g_id})
        db.eg4.update_one({"g_id":g_id},
                           {"$set": {"eqtl_gwas_number": len(tmp_result)}})





def update_predict_sample_number():
    #dd = db.eg4.distinct('g_id')
    f = open("/NAS/yulix/20230804_G4database/result/hg.pqs.group.result","r")
    header = f.readline().strip("\n").split("\t")
    mm = 0
    for aaa in db.predicted_Human.find(no_cursor_timeout=True):
        line = f.readline()
        fields = line.rstrip("\n").split("\t")
        record = dict(zip(header, fields))
        g_id = record['id'].replace("ID","HG4")
        # if g_id not in dd:
        #     continue
        del record['id']
        del record['chr']
        del record['start']
        del record['end']
        del record['score']
        del record['strand']
        aaa['sample_number'] = record['sum']
        del record['sum']
        del aaa['_id']
        db.predicted_Human2.insert_one(aaa)
        if record['group']=="Non-eG4":
            continue
        del record['group']
        samples = []
        for i in record.keys():
            if record[i]!="0":
                samples.append(i)
        db.eg4.update_one({"g_id": g_id},
                   {"$set": {"sample_number": len(samples),"detect_samples":samples}})
db.eg4.update_one({"g_id": "HG4_1443231"},
                   {"$set": {"sample_number": 28,"detect_samples":['AB521M', 'AB551', 'AB555M', 'AB577M', 'AB636M', 'AB790', 'CNCC', 'H1975_G4chip', 'HACAT_Entinostat', 'HCI009', 'HEK293T_Flavopiridol.CUT.Tag_FP', 'HEK293T_PDS.CUT.Tag_DMSO', 'HEK293T_PDS.CUT.Tag_PDS', 'iPSC.derived_neurons', 'K562_TPL', 'NSC', 'PAR1006', 'STG139', 'STG139M_181', 'STG143_317', 'STG201_181', 'STG201_284', 'STG331', 'VHIO098_181', 'VHIO179_181', 'VHIO179_284', 'HACAT_NA', 'HEK293T']}})
db.eg4.update_one({"g_id": "HG4_1443257"},
                   {"$set": {"sample_number": 28,"detect_samples":['A549_G4chip', 'AB521M', 'AB551', 'AB555M', 'AB577M', 'AB636M', 'AB863M', 'CNCC', 'ESC', 'H1975_G4chip', 'HACAT_Entinostat', 'HEK293T_Flavopiridol.CUT.Tag_DMSO', 'HEK293T_Flavopiridol.CUT.Tag_FP', 'HEK293T_PDS.CUT.Tag_DMSO', 'HEK293T_PDS.CUT.Tag_PDS', 'iPSC.derived_neurons', 'K562_TPL', 'NSC', 'STG139', 'STG139M_181', 'STG139M_284', 'STG201_181', 'STG201_284', 'STG331', 'VHIO098_181', 'VHIO179_181', 'VHIO179_284', 'HACAT_NA']}})
db.eg4.update_one({"g_id": "HG4_1443258"},
                   {"$set": {"sample_number": 31,"detect_samples":['A549_G4chip', 'AB521M', 'AB551', 'AB555M', 'AB577M', 'AB580', 'AB636M', 'AB790', 'AB863M', 'CNCC', 'ESC', 'H1975_G4chip', 'HACAT_Entinostat', 'HEK293T_Flavopiridol.CUT.Tag_DMSO', 'HEK293T_Flavopiridol.CUT.Tag_FP', 'HEK293T_PDS.CUT.Tag_DMSO', 'HEK293T_PDS.CUT.Tag_PDS', 'iPSC.derived_neurons', 'K562_TPL', 'NSC', 'STG139', 'STG139M_181', 'STG139M_284', 'STG143_317', 'STG201_181', 'STG201_284', 'STG331', 'VHIO098_181', 'VHIO179_181', 'VHIO179_284', 'HACAT_NA']}})
for i in db.eg4.find({"detect_samples":"iPSC.derived_neurons_1H6_AD"}):
    i['detect_samples'].remove("iPSC.derived_neurons_1H6_AD")
    i['detect_samples'].append("iPSC.derived_neurons")
    db.eg4.update_one({"g_id": i['g_id']},
                                  {"$set": {"detect_samples": i['detect_samples']}})

for i in db.eg4.find({"detect_samples":"X93T449.BG4"}):
    i['detect_samples'].remove("X93T449.BG4")
    i['detect_samples'].append("93T449.BG4")
    db.eg4.update_one({"g_id": i['g_id']},
                                  {"$set": {"detect_samples": i['detect_samples']}})


db.predicted_Human.drop()
db.predicted_Human2.rename("predicted_Human")

db.predicted_Human.update_one({"g_id": "HG4_1443231"},
                   {"$set": {"sample_number": 28}})
db.predicted_Human.update_one({"g_id": "HG4_1443257"},
                   {"$set": {"sample_number": 28}})
db.predicted_Human.update_one({"g_id": "HG4_1443258"},
                   {"$set": {"sample_number": 31}})


# 为了复合sample.list，更正了/NAS/yulix/20230804_G4database/result/m.pqs_G4.txt的header
def update_sample_number():
    dd = db.meg4.distinct('g_id')
    f = open("/NAS/yulix/20230804_G4database/result/m.pqs_G4.txt","r")
    header = f.readline().strip("\n").split("\t")
    mm = 0
    for line in f:
        fields = line.rstrip("\n").split("\t")
        record = dict(zip(header, fields))
        g_id = record['name.1'].replace("id","MG4")
        if g_id not in dd:
            continue
        record['sum'] = int(record['sum'])
        if record['sum']>=6:
            glevel = "Level6"
        else:
            glevel = "Level" + str(record['sum'])
        del record['name.1']
        del record['chr']
        del record['start']
        del record['end']
        del record['score']
        del record['strand']
        del record['sum']
        samples = []
        for i in record.keys():
            if record[i]!="0":
                samples.append(i)
        db.meg4.update_one({"g_id": g_id},
                   {"$set": {"sample_number": len(samples),"detect_samples":samples,
                             "group":glevel}})

db.predicted_Chicken.update_many({}, {"$set": {"sample_number": 0}})
db.predicted_Human.create_index([("g_id",1)])
def human_predict_number():
    db.predicted_Human.update_many({},{"$set": {"sample_number": 0}})
    for record in db.eg4.find(no_cursor_timeout=True).batch_size(100):
        db.predicted_Human.update_one({"g_id": record['g_id']},
                   {"$set": {"sample_number": int(record["sample_number"]),
                             "group":record["group"]}})


def mouse_predict_number():
    db.predicted_Mouse.update_many({}, {"$set": {"sample_number": 0}})
    for record in db.meg4.find(no_cursor_timeout=True).batch_size(100):
        db.predicted_Mouse.update_one({"g_id": record['g_id']},
                                      {"$set": {"sample_number": int(record["sample_number"]),
                                                "group": record["group"]}})

# def chicken_predict_number():
#     #db.ceg4.update_many({}, {"$set": {"sample_number": 1}})
#     #db.predicted_Chicken.update_many({}, {"$set": {"sample_number": 0}})
#     for record in db.ceg4.find(no_cursor_timeout=True).batch_size(100):
#         db.predicted_Chicken.update_one({"g_id": record['g_id']},
#                    {"$set": {"sample_number": record["sample_number"]}})
#
# db.predicted_Mouse.update_many({}, {"$set": {"sample_number": 0}})
# 在eg4导入时直接写入更快



update_dbs = []
for dbname in db.collection_names():
    tmpres = db[dbname].find_one()
    if "group" in tmpres.keys():
        update_dbs.append(dbname)

for dbname in update_dbs:
    for item in db[dbname].find():
        _id = item['_id']
        group = item['group']
        group = str(group).replace('level', 'Level')
        db[dbname].update_one({'_id':_id},
                              {"$set": {"group": group}})



for i in db.eg4.distinct("gene_type"):
    if "pseudogene" in i:
        db.eg4.update_many({"gene_type": i},
                                       {"$set": {"gene_type": "pseudogene"}})

for i in db.predicted_Human.distinct("gene_type"):
    if "pseudogene" in i:
        db.predicted_Human.update_many({"gene_type": i},
                                       {"$set": {"gene_type": "pseudogene"}})

for i in db.ceg4.distinct("gene_type"):
    if "pseudogene" in i:
        db.ceg4.update_many({"gene_type": i},
                                       {"$set": {"gene_type": "pseudogene"}})

for i in db.predicted_Chicken.distinct("gene_type"):
    if "pseudogene" in i:
        db.predicted_Chicken.update_many({"gene_type": i},
                                       {"$set": {"gene_type": "pseudogene"}})

for i in db.meg4.distinct("gene_type"):
    if "pseudogene" in i:
        db.meg4.update_many({"gene_type": i},
                                       {"$set": {"gene_type": "pseudogene"}})

for i in db["predicted_Zebrafish"].distinct("gene_type"):
    if "pseudogene" in i:
        db["predicted_Zebrafish"].update_many({"gene_type": i},
                                       {"$set": {"gene_type": "pseudogene"}})



def updatepredict(Species):
    for i in db[Species].find():
        del i["_id"]
        db[f'{Species}_new'].insert_one(i)
    db[Species].drop()
    db[f'{Species}_new'].rename(Species)

from pymongo.collation import Collation
def updatepredict(Species):
    for i in db[Species].find().sort([("g_id", "desc")]).collation(Collation(locale='en_US', numericOrdering = True)).batch_size(100):
        del i["_id"]
        db[f'{Species}_new'].insert_one(i)
    #db[Species].drop()
    #db[f'{Species}_new'].rename(Species)

updatepredict("predicted_Human")

for i in db.predicted_Human.find():
    del i["_id"]
    i["sample_number"] = int(i["sample_number"])
    db.predicted_Human2.insert_one(i)

db.predicted_Human.drop()
db.predicted_Human2.rename("predicted_Human")