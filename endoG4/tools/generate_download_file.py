import pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.endoG4


def predicted(species):
    species = species.replace(" ","_")
    file_path = "/home/shimw/web/G4-portal/endoG4/static/Predicted_" + species.lower()+"_G4.txt"
    predicted_file = open(file_path, "w")
    if species in ["Human","Mouse","Chicken"]:
        predicted_file.write("\t".join(
            ["Chr", "Start", "End", "Strand", "G4 id", "Score", "Confidence level",
        "Gene", "Symbol", "Gene Type", "Size", "phastCons", "phyloP",
        "cell number", "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
             ]) + "\n")

        for i in db["predicted_" + species].find():
            predicted_file.write("\t".join([i['chr'], str(i['start']), str(i['end']), i['strand'],i['g_id'],str(i['score']), i['group'],
                                        i['gene_id'], i['gene_name'],i["gene_type"],
                                            str(i["size"]),str(i["phastCons"]),str(i["phyloP"]),str(i["sample_number"]),str(i["rl1"]),
                                            str(i["rl2"]),str(i["rl3"]),str(i["ll1"]),str(i["ll2"]),str(i["ll3"]),i["seq"]]) + "\n")
    if species in ["Fruit_fly", "C._elegans"]:
        predicted_file.write("\t".join(
            ["Chr", "Start", "End", "Strand", "G4 id", "Score",
        "Gene", "Symbol", "Gene Type", "Size", "phastCons", "phyloP",
        "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
             ]) + "\n")

        for i in db["predicted_" + species].find():
            predicted_file.write("\t".join([i['chr'], str(i['start']), str(i['end']), i['strand'],i['g_id'],str(i['score']),
                                        i['gene_id'], i['gene_name'],i["gene_type"],
                                            str(i["size"]),str(i["phastCons"]),str(i["phyloP"]),str(i["rl1"]),
                                            str(i["rl2"]),str(i["rl3"]),str(i["ll1"]),str(i["ll2"]),str(i["ll3"]),i["seq"]]) + "\n")
    if species in ["Pig","Rhesus_macaque", "Rat", "Rabbit", "Opossums", "Zebrafish"]:
        predicted_file.write("\t".join(
            ["Chr", "Start", "End", "Strand", "G4 id", "Score",
        "Gene", "Symbol", "Gene Type", "Size",
        "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
             ]) + "\n")
        for i in db["predicted_" + species].find():
            predicted_file.write("\t".join([i['chr'], str(i['start']), str(i['end']), i['strand'],i['g_id'],str(i['score']),
                                        i['gene_id'], i['gene_name'],i["gene_type"],
                                            str(i["size"]),str(i["rl1"]),
                                            str(i["rl2"]),str(i["rl3"]),str(i["ll1"]),str(i["ll2"]),str(i["ll3"]),i["seq"]]) + "\n")

    predicted_file.close()


predicted("Human")
predicted("Mouse")
predicted("Pig")
predicted("Chicken")
predicted("Rhesus macaque")
predicted("Rat")
predicted("Rabbit")
predicted("Opossums")
predicted("Zebrafish")
predicted("Fruit fly")
predicted("C. elegans")




def endoG4():
    endoG4_file = open("/home/shimw/web/G4-portal/endoG4/static/Human_eG4.txt", "w")
    bed_file = open("/home/shimw/web/G4-portal/endoG4/static/Human_eG4.bed", "w")
    endoG4_file.write("\t".join(
        ["Chr","Start", "End", "Strand", "G4 id", "Score", "Confidence level",
         "Gene", "Symbol", "Gene Type", "Size", "phastCons", "phyloP",
         "cell number", "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
         ]) + "\n")
    for i in db.eg4.find():
        endoG4_file.write("\t".join([i['chr'], str(i['start']), str(i['end']), i['strand'],i["g_id"],str(i['score']),i['group'],
                                    i['gene_id'], i['gene_name'],i["gene_type"],str(i["size"]),str(i["phastCons"]),str(i["phyloP"]),str(i["sample_number"]),str(i["rl1"]),
                                            str(i["rl2"]),str(i["rl3"]),str(i["ll1"]),str(i["ll2"]),str(i["ll3"]),i["seq"]]) + "\n")
        bed_file.write("\t".join([i['chr'], str(i['start']-1), str(i['end']), i["g_id"],str(i['score']),i["strand"]]) + "\n")
    endoG4_file.close()
    bed_file.close()


def MendoG4():
    endoG4_file = open("/home/shimw/web/G4-portal/endoG4/static/Mouse_eG4.txt", "w")
    bed_file = open("/home/shimw/web/G4-portal/endoG4/static/Mouse_eG4.bed", "w")
    endoG4_file.write("\t".join(
        ["Chr","Start", "End", "Strand", "G4 id", "Score", "Confidence level",
         "Gene", "Symbol", "Gene Type", "Size", "phastCons", "phyloP",
         "cell number", "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
         ]) + "\n")
    for i in db.meg4.find():
        endoG4_file.write("\t".join([i['chr'], str(i['start']), str(i['end']), i['strand'],i["g_id"],str(i['score']),i['group'],
                                    i['gene_id'], i['gene_name'],i["gene_type"],str(i["size"]),str(i["phastCons"]),str(i["phyloP"]),str(i["rl1"]),
                                            str(i["rl2"]),str(i["rl3"]),str(i["ll1"]),str(i["ll2"]),str(i["ll3"]),i["seq"]]) + "\n")
        bed_file.write("\t".join([i['chr'], str(i['start']-1), str(i['end']), i["g_id"],str(i['score']),i["strand"]]) + "\n")
    endoG4_file.close()
    bed_file.close()

def GendoG4():
    endoG4_file = open("/home/shimw/web/G4-portal/endoG4/static/Chicken_eG4.txt", "w")
    bed_file = open("/home/shimw/web/G4-portal/endoG4/static/Chicken_eG4.bed", "w")
    endoG4_file.write("\t".join(
        ["Chr","Start", "End", "Strand", "G4 id", "Score", "Confidence level",
         "Gene", "Symbol", "Gene Type", "Size", "phastCons", "phyloP",
         "cell number", "rl1", "rl2", "rl3", "ll1", "ll2", "ll3", "seq"
         ]) + "\n")
    for i in db.ceg4.find():
        endoG4_file.write("\t".join([i['chr'], str(i['start']), str(i['end']), i['strand'],i["g_id"],str(i['score']),i['group'],
                                    i['gene_id'], i['gene_name'],i["gene_type"],str(i["size"]),str(i["phastCons"]),str(i["phyloP"]),str(i["rl1"]),
                                            str(i["rl2"]),str(i["rl3"]),str(i["ll1"]),str(i["ll2"]),str(i["ll3"]),i["seq"]]) + "\n")
        bed_file.write("\t".join([i['chr'], str(i['start']-1), str(i['end']), i["g_id"],str(i['score']),i["strand"]]) + "\n")
    endoG4_file.close()
    bed_file.close()

# endoG4()
def Epigenetics():
    file1 = "/home/shimw/chromHMM_6groups"
    file2 = "/home/shimw/DHS_6groups"
    file3 = "/home/shimw/H3K27ac_6groups"
    cmd = "tar czvfP /home/shimw/web/G4-portal/endoG4/static/endoG4_Epigenetics.gz %s %s %s" % (file1,
                                                                                                file2,
                                                                                                file3)
    os.system(cmd)

def TF():
    file1 = "/home/shimw/Group1"
    file2 = "/home/shimw/Group2"
    file3 = "/home/shimw/Group3"
    file4 = "/home/shimw/Group4"
    file5 = "/home/shimw/Group5"
    file6 = "/home/shimw/Group6"
    cmd = "tar czvfP /home/shimw/web/G4-portal/endoG4/static/endoG4_TF.gz %s %s %s %s %s %s" % (file1,
                                                                                                file2,
                                                                                                file3,
                                                                                                file4,
                                                                                                file5,
                                                                                                file6)
    os.system(cmd)

def snp():
    cmd = "cp /NAS/yulix/all_G4_data/01.G4_pqs/6groups.GWAS.hg19.txt /home/shimw/web/G4-portal/endoG4/static/endoG4_GWAS_SNP.txt"
    os.system(cmd)
    cmd = "cp /NAS/yulix/all_G4_data/01.G4_pqs/6groups.cis.txt /home/shimw/web/G4-portal/endoG4/static/endoG4_GTEx_eQTL.txt"
    os.system(cmd)
    cmd = "cp /NAS/yulix/all_G4_data/01.G4_pqs/6groups.GTEx.txt /home/shimw/web/G4-portal/endoG4/static/endoG4_cancer_eQTL.txt"
    os.system(cmd)
    cmd = "cp /home/yulix/G4_analysis/result/savedata2/pqs.intersect.narrowpeak/narrowPeak.tar.gz /home/shimw/web/G4-portal/endoG4/static/narrowPeak.tar.gz"
    os.system(cmd)




