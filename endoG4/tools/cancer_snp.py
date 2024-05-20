f = open("/home/shimw/survival-eQTL_all_data.txt")
"/NAS/yulix/all_G4_data/01.G4_pqs/6groups.cis.txt"
for line in f:
    line = line.strip().split("\t")
    rsid = line[1]
