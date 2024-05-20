import pandas as pd
import glob

# 找到所有BED文件
bed_files = glob.glob("/home/shimw/pqsdata/*/*pqs.sort.bed")

for bed_file in bed_files:
    # 读取BED文件
    df = pd.read_csv(bed_file, sep='\t', header=None)

    # 将起始位置列（通常是第二列，Python索引从0开始）减1
    df[1] = df[1] - 1

    # 写回文件
    df.to_csv(bed_file, sep='\t', header=False, index=False)

txt_file ="/home/shimw/web/G4-portal/endoG4/static/Predicted_human_G4.txt"
bed_file = "/home/shimw/web/G4-portal/endoG4/static/Predicted_human_G4.bed"
df = pd.read_csv(txt_file, sep='\t')
df["start"] = df["start"] - 1
new_df = df[["chr", "start", "end", "gene_id", "score", "strand"]]
new_df["gene_id"] = "."
new_df.to_csv(bed_file, sep='\t', header=False, index=False)