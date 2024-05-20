/home/yulix/G4_analysis/result/savedata2/GTEx/GTEx_Analysis_v7_eQTL/
"/home/qians/Pseudo/Data/Seqdata/GWAS/gwas_catalog_v1.0-associations_e100_r2021-02-25.tsv"
cd /home/shimw/project/mengwei_G4/data/SNP
bedtools sort -i GTEx.bed |uniq > GTEx.uniq.bed
bedtools intersect -a /home/shimw/project/mengwei_G4/data/SNP/GTEx.uniq.bed -b /home/shimw/project/mengwei_G4/result/hg.eG4.bed  -wa -wb > G4.GTEx.txt
