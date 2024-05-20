bigWigAverageOverBed mm10.60way.phyloP60way.bw m.G4.bed mm_G4.phyloP
bigWigAverageOverBed mm10.60way.phyloP60way.bw m.G4.bed mm_G4.phyloP
# Pig susScr11  no conservation
# Chicken galGal6
https://hgdownload.soe.ucsc.edu/goldenPath/galGal6/phastCons77way/galGal6.phastCons77way.bw
https://hgdownload.soe.ucsc.edu/goldenPath/galGal6/phyloP77way/galGal6.phyloP77way.bw
# Rhesus macaque rheMac10 no conservation
# Rat rn7 no conservation
# Rabbit oryCun2 no conservation
# Fruit fly  dm6
https://hgdownload.soe.ucsc.edu/goldenPath/dm6/phastCons124way/dm6.phastCons124way.bw
https://hgdownload.soe.ucsc.edu/goldenPath/dm6/phyloP124way/dm6.phyloP124way.bw
# C. elegans ce11
https://hgdownload.soe.ucsc.edu/goldenPath/ce11/phastCons135way/ce11.phastCons135way.bw
https://hgdownload.soe.ucsc.edu/goldenPath/ce11/phyloP135way/ce11.phyloP135way.bw
# 只有多的三个物种有conservation的信息

mkdir /home/shimw/project/mengwei_G4/data/conservation/
# wget 上面链接
cut -f1-4 /home/shimw/project/mengwei_G4/data/pqs/C_elegans.sort.pqs_gene.txt > /home/shimw/project/mengwei_G4/data/pqs/C_elegans.simple.bed
bigWigAverageOverBed "/home/shimw/project/mengwei_G4/data/conservation/ce11.phastCons135way.bw"\
 "/home/shimw/project/mengwei_G4/data/pqs/C_elegans.simple.bed" /home/shimw/project/mengwei_G4/data/conservation/C_elegans.phastCons
bigWigAverageOverBed "/home/shimw/project/mengwei_G4/data/conservation/ce11.phyloP135way.bw"\
 "/home/shimw/project/mengwei_G4/data/pqs/C_elegans.simple.bed" /home/shimw/project/mengwei_G4/data/conservation/C_elegans.phyloP

cut -f1-4 /home/shimw/project/mengwei_G4/data/pqs/chicken.sort.pqs_gene.txt > /home/shimw/project/mengwei_G4/data/pqs/chicken.simple.bed
bigWigAverageOverBed "/home/shimw/project/mengwei_G4/data/conservation/galGal6.phastCons77way.bw"\
 "/home/shimw/project/mengwei_G4/data/pqs/chicken.simple.bed" /home/shimw/project/mengwei_G4/data/conservation/chicken.phastCons
bigWigAverageOverBed "/home/shimw/project/mengwei_G4/data/conservation/galGal6.phyloP77way.bw"\
 "/home/shimw/project/mengwei_G4/data/pqs/chicken.simple.bed" /home/shimw/project/mengwei_G4/data/conservation/chicken.phyloP

cut -f1-4 /home/shimw/project/mengwei_G4/data/pqs/drosophila_melanogaster.sort.pqs_gene.txt > /home/shimw/project/mengwei_G4/data/pqs/drosophila_melanogaster.simple.bed
bigWigAverageOverBed "/home/shimw/project/mengwei_G4/data/conservation/dm6.phastCons124way.bw"\
 "/home/shimw/project/mengwei_G4/data/pqs/drosophila_melanogaster.simple.bed" /home/shimw/project/mengwei_G4/data/conservation/drosophila_melanogaster.phastCons
bigWigAverageOverBed "/home/shimw/project/mengwei_G4/data/conservation/dm6.phyloP124way.bw"\
 "/home/shimw/project/mengwei_G4/data/pqs/drosophila_melanogaster.simple.bed" /home/shimw/project/mengwei_G4/data/conservation/drosophila_melanogaster.phyloP

cut -f1-4 /home/shimw/pqsdata/human/human.sort.pqs_gene.txt > /home/shimw/project/mengwei_G4/data/pqs/human.simple.bed
bigWigAverageOverBed "/home/yulix/G4_analysis/analysis/bw_file/hg19.100way.phastCons.bw" \
/home/shimw/project/mengwei_G4/data/pqs/human.simple.bed /home/shimw/project/mengwei_G4/data/conservation/Human.phastCons
bigWigAverageOverBed "/home/yulix/G4_analysis/analysis/bw_file/hg19.100way.phyloP100way.bw" \
/home/shimw/project/mengwei_G4/data/pqs/human.simple.bed /home/shimw/project/mengwei_G4/data/conservation/Human.phyloP


cut -f1-4 /home/shimw/pqsdata/mouse/mouse.sort.pqs_gene.txt > /home/shimw/project/mengwei_G4/data/pqs/mouse.simple.bed
bigWigAverageOverBed "/NAS/yulix/mengwei_G4/result/mm10.60way.phastCons.bw" \
/home/shimw/project/mengwei_G4/data/pqs/mouse.simple.bed /home/shimw/project/mengwei_G4/data/conservation/Mouse.phastCons
bigWigAverageOverBed "/NAS/yulix/mengwei_G4/result/mm10.60way.phyloP60way.bw" \
/home/shimw/project/mengwei_G4/data/pqs/mouse.simple.bed /home/shimw/project/mengwei_G4/data/conservation/Mouse.phyloP






