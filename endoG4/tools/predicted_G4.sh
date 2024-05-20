# 基因的bed文件构建
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/shimw/pqsdata/C_elegans/Caenorhabditis_elegans.WBcel235.109.gtf" >"/home/shimw/pqsdata/C_elegans/C_elegans.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/shimw/pqsdata/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.32.109.chr.gtf" >"/home/shimw/pqsdata/drosophila_melanogaster/drosophila_melanogaster.gene.bed"
sed -i 's/^/chr/g' /home/shimw/pqsdata/drosophila_melanogaster/drosophila_melanogaster.gene.bed
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/shimw/pqsdata/opossum/Monodelphis_domestica.ASM229v1.109.chr.gtf" >"/home/shimw/pqsdata/opossum/opossum.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/shimw/pqsdata/rabbit/Oryctolagus_cuniculus.OryCun2.0.109.chr.gtf" >"/home/shimw/pqsdata/rabbit/rabbit.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/shimw/pqsdata/rat/Rattus_norvegicus.mRatBN7.2.109.chr.gtf" >"/home/shimw/pqsdata/rat/rat.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py /home/shimw/pqsdata/rhesus_macaque/Macaca_mulatta.Mmul_10.109.chr.gtf >/home/shimw/pqsdata/rhesus_macaque/rhesus_macaque.gene.bed
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/shimw/pqsdata/zebrafish/Danio_rerio.GRCz11.109.chr.gtf" >"/home/shimw/pqsdata/zebrafish/zebrafish.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py /home/yulix/G4_analysis/data/ref/Gallus_gallus/Gallus_gallus.GRCg6a.104.chr.gtf >"/home/shimw/pqsdata/chicken.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/NAS/yulix/all_G4_data/ref/Sus_scrofa.Sscrofa11.1.107.chr.gtf" >"/home/shimw/pqsdata/pig/pig.gene.bed"

# 不是ensembl下的，所以去掉了chr添加
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/yulix/G4_analysis/data/ref/gencode.v38lift37.annotation.gtf" >"/home/shimw/pqsdata/human/human.gene.bed"
python ~/web/G4-portal/endoG4/tools/get_gene_bed.py "/home/yulix/G4_analysis/data/ref/M10/gencode.vM10.annotation.gtf" >"/home/shimw/pqsdata/mouse/mouse.gene.bed"




for i in `ls /home/shimw/pqsdata/`
do
  cd /home/shimw/pqsdata/$i
bedtools sort -i ${i}.gene.bed > ${i}.gene.sort.bed
done


bedtools sort -i gallus.G4.bed > gallus_G4.sort.bed
bedtools sort -i gallus.pqs.bed > gallus_pqs.sort.bed
bedtools sort -i /home/shimw/pqsdata/chicken/chicken.gene.bed > /home/shimw/pqsdata/chicken/chicken.gene.sort.bed
bedtools closest -a gallus_G4.sort.bed -b /home/yulix/G4_analysis/data/ref/Gallus_gallus/galllus_gene.sort.bed -d > galllus_G4_gene.txt
bedtools closest -a /NAS/yulix/20230804_G4database/result/gallus_pqs_all.bed -b /home/shimw/pqsdata/chicken/chicken.gene.sort.bed -d > /home/shimw/pqsdata/chicken/chicken.pqs_gene.txt






for i in `ls /home/shimw/pqsdata/`
  do
   cd /home/shimw/pqsdata/$i
    bedtools sort -i ${i}.pqs.bed > ${i}.pqs.sort.bed
    bedtools closest -a ${i}.pqs.sort.bed -b ${i}.gene.sort.bed -d > ${i}.pqs_gene.txt
    awk '!a[$4]++{print}' ${i}.pqs_gene.txt > ${i}.sort.pqs_gene.txt
  done

cp /home/shimw/pqsdata/*/*.sort.pqs_gene.txt ~/project/mengwei_G4/data/pqs/

## 小鼠pqs
bedtools closest -a /NAS/yulix/20230804_G4database/result/m_pqs_all.bed\
 -b /NAS/yulix/20230804_G4database/result/mouse_gene.bed\
  -d > /home/shimw/project/mengwei_G4/data/pqs/mouse_pqs_gene.txt

sort -k1,1 -k2,2n /NAS/yulix/20230804_G4database/result/hg_pqs_table.tsv > /home/shimw/pqsdata/human/human.pqs.sort.bed
bedtools closest -a /home/shimw/pqsdata/human/human.pqs.sort.bed\
 -b /home/shimw/pqsdata/human/human.gene.sort.bed\
  -d > /home/shimw/pqsdata/human/human.pqs_gene.txt
  awk '!a[$4]++{print}' human.pqs_gene.txt > /home/shimw/pqsdata/human/human.sort.pqs_gene.txt


sort -k1,1 -k2,2n /NAS/yulix/20230804_G4database/result/m.G4.bed > /home/shimw/pqsdata/mouse/mouse.eG4.sort.bed
sort -k1,1 -k2,2n /NAS/yulix/20230804_G4database/result/m_pqs_all.bed > /home/shimw/pqsdata/mouse/mouse.pqs.sort.bed
bedtools closest -a /home/shimw/pqsdata/mouse/mouse.pqs.sort.bed\
 -b /home/shimw/pqsdata/mouse/mouse.gene.sort.bed\
  -d > /home/shimw/pqsdata/mouse/mouse.pqs_gene.txt
  awk '!a[$4]++{print}' mouse.pqs_gene.txt > /home/shimw/pqsdata/mouse/mouse.sort.pqs_gene.txt

sort -k1,1 -k2,2n /NAS/yulix/20221102cut-tag/result/peak_deal/pig/pig_pqs_all.bed > /home/shimw/pqsdata/pig/pig.pqs.sort.bed
sed -i 's/^/chr/' /home/shimw/pqsdata/pig/pig.pqs.sort.bed
bedtools closest -a /home/shimw/pqsdata/pig/pig.pqs.sort.bed\
 -b /home/shimw/pqsdata/pig/pig.gene.sort.bed\
  -d > /home/shimw/pqsdata/pig/pig.pqs_gene.txt
  awk '!a[$4]++{print}' pig.pqs_gene.txt > /home/shimw/pqsdata/pig/pig.sort.pqs_gene.txt

