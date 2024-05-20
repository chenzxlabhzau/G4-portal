import sys,os
import pandas as pd
import csv
import re
import json

files = os.listdir("/home/xlpan/CRC/ChIP-seq/tumor/")
dirpath = "/home/xlpan/CRC/ChIP-seq/tumor/"
ids =list(set([c.split("-")[0] for c in files]))

for mm in ids:
    kk = list(set([c.split("-")[1].split("_")[0] for c in files if c.startswith(mm) and 'Input' not in c]))
    for nn in kk:
        ll = {"GEO": "wuda", "GSM": mm, "TUSSUE": "colon", "CANCER_TYPE": "colorectal cancer",
         "fq": {"fq1": dirpath + mm + "-" + nn +"_R1.fastq.gz",
                "fq2": dirpath + mm + "-" + nn +"_R2.fastq.gz"},
              "INPUT": {"fq1": dirpath + mm + "-Input_R1.fastq.gz",
                "fq2": dirpath + mm + "-Input_R2.fastq.gz"}, "normal": None,
         "norinp": None, "layout": "PAIRED"}
        with open("/home/mwshi/project/conservation/new_metajson/" + mm+ "_"+ nn + ".json", 'w') as w:
            json.dump(ll, w)





files = os.listdir("/home/xlpan/CRC/ChIP-seq/native/")
dirpath = "/home/xlpan/CRC/ChIP-seq/native/"
ids =list(set([c.split("-")[0] for c in files if c.endswith("gz")]))

for mm in ids:
    kk = list(set([c.split("-")[1].split("_")[0] for c in files if c.startswith(mm) and 'Input' not in c]))
    for nn in kk:
        ll = {"GEO": "wuda", "GSM": mm, "TUSSUE": "colon", "CANCER_TYPE": "colorectal cancer",
         "fq": {"fq1": dirpath + mm + "-" + nn +"_R1.fastq.gz",
                "fq2": dirpath + mm + "-" + nn +"_R2.fastq.gz"},
              "INPUT": {"fq1": dirpath + mm + "-Input_R1.fastq.gz",
                "fq2": dirpath + mm + "-Input_R2.fastq.gz"}, "normal": None,
         "norinp": None, "layout": "PAIRED"}
        with open("/home/mwshi/project/conservation/new_metajson/" + mm+ "_"+ nn + ".json", 'w') as w:
            json.dump(ll, w)