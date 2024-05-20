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

## 五个物种需要使用conservation的表格



#filepath = "/NAS/luozh/CancerEnhancerDB/step10_all_narrow_peak/all_narrow_peaks_gene_annotation/"
def import_predicted(filepath,species,fasta_file):
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    GeId_dict = {"C. elegans":"CEG4", "Fruit fly":"FG4","Opossums":"OG4",
                 "Rabbit":"RBG4", "Rat":"RG4","Rhesus macaque":"RMG4",
                 "Zebrafish":"ZG4","Chicken":"CG4","Pig":"PG4"}
    # 这里我手动按照species改了一下名字
    if species in ["Fruit fly", "C. elegans", "Chicken", "Human", "Mouse"]:
        phastCons=open(f"/home/shimw/project/mengwei_G4/data/conservation/{species}.phastCons", "r")
        phyloP = open(f"/home/shimw/project/mengwei_G4/data/conservation/{species}.phyloP", "r")
    with open(filepath, "r") as reader:
        db["predicted_" + species.replace(" ","_")].drop()
        # 聿力给的物种score在第七列，length在第五列，和泽昊的不同
        header = ["chr", "start","end","g_id","size","strand","score","nt","nb","nm",
                  "rl1","rl2","rl3","ll1","ll2","ll3","a","b", "c", "d","gene_id","gene_name","gene_type", "e"]
        # if species=="Pig":
        #     header = ["chr", "start", "end", "g_id", "score", "strand", "a", "b", "c","d", "gene_id", "gene_name",
        #               "gene_type"]
        i=0
        for line in reader:
            i = i +1
            fields = line.rstrip("\n").split("\t")
            record = dict(zip(header, fields))
            for k in record:
                if k in ["size","start", "end", "score","rl1","rl2","rl3","ll1","ll2","ll3"]:
                    record[k] = int(record[k])
            del record["a"]
            del record["b"]
            del record["c"]
            del record["d"]
            del record["e"]
            del record["nt"]
            del record["nb"]
            del record["nm"]
            if species=="Chicken":
                record["g_id"] = record["g_id"].replace("g", GeId_dict[species])
            elif species=="Pig":
                record["g_id"] = record["g_id"].replace("pig", GeId_dict[species])
            else:
                record["g_id"] = record["g_id"].replace("id", GeId_dict[species])
            record["seq"] = get_sequence_from_fasta(record_dict,record["chr"].replace("chr", ""), record["start"], record["end"], record["strand"])
            if "pseudogene" in record['gene_type']:
                record['gene_type'] = "pseudogene"
            record["gene_id"]=record["gene_id"].split(".")[0]
            if record['gene_name'].isdigit() or record['gene_name']=="NA":
                record['gene_name']=""
            if species in ["Fruit fly", "C. elegans", "Chicken", "Human", "Mouse"]:
                record["phastCons"] = phastCons.readline().strip().split("\t")[5]
                record["phyloP"] = phyloP.readline().strip().split("\t")[5]
            db["predicted_" + species.replace(" ","_")].insert_one(record)

## 合并
## cat /home/yulix/G4_analysis/result/savedata2/pqs.intersect.narrowpeak/pqs_gene.txt /NAS/yulix/all_G4_data/01.G4_pqs/G4_gene.txt > /home/shimw/predict_G4.bed
## sort -k1,1 -k2,2n /home/shimw/predict_G4.bed > /home/shimw/predict_G4.sorted.bed



import_predicted("/home/shimw/project/mengwei_G4/data/pqs/C_elegans.sort.pqs_gene.txt","C. elegans", "/home/shimw/pqsdata/C_elegans/Caenorhabditis_elegans.WBcel235.dna.chr.fa")
import_predicted("/home/shimw/project/mengwei_G4/data/pqs/drosophila_melanogaster.sort.pqs_gene.txt","Fruit fly", "/home/shimw/pqsdata/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.32.dna.chr.fa")
import_predicted("/home/shimw/project/mengwei_G4/data/pqs/opossum.sort.pqs_gene.txt","Opossums", "/home/shimw/pqsdata/opossum/Monodelphis_domestica.ASM229v1.dna.chr.fa")
import_predicted("/home/shimw/project/mengwei_G4/data/pqs/rabbit.sort.pqs_gene.txt","Rabbit","/home/shimw/pqsdata/rabbit/Oryctolagus_cuniculus.OryCun2.0.dna.chr.fa")
import_predicted("/home/shimw/project/mengwei_G4/data/pqs/rat.sort.pqs_gene.txt", "Rat", "/home/shimw/pqsdata/rat/Rattus_norvegicus.mRatBN7.2.dna.chr.fa")
import_predicted("/home/shimw/project/mengwei_G4/data/pqs/rhesus_macaque.sort.pqs_gene.txt", "Rhesus macaque", "/home/shimw/pqsdata/rhesus_macaque/Macaca_mulatta.Mmul_10.dna.chr.fa")
import_predicted("/home/shimw/project/mengwei_G4/data/pqs/zebrafish.sort.pqs_gene.txt", "Zebrafish", "/home/shimw/pqsdata/zebrafish/Danio_rerio.GRCz11.dna.chr.fa")

# import_predicted("/home/shimw/predict_G4.sorted.bed","Human")  现在人类的G4 predict需要重新重新写
# import_predicted("/home/yulix/G4_analysis/result/savedata2/mouse/mouse_pqs_gene.txt","Mouse")
# import_predicted("/home/shimw/project/mengwei_G4/data/pqs/chicken.sort.pqs_gene.txt", "Chicken", "/home/yulix/G4_analysis/data/ref/Gallus_gallus/Gallus_gallus.genome.fa")
import_predicted("/home/shimw/pqsdata/pig/pig.sort.pqs_gene.txt","Pig", "/NAS/yulix/all_G4_data/ref/Sus_scrofa.Sscrofa11.1.dna_sm.toplevel.fa")



