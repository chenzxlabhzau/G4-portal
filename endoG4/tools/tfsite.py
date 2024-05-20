import pandas as pd

chunksize = 10 ** 6  # 调整此值以适应你的系统
filename = '/opt/shimw/Human.macs2.clusters.interval.merge3.hg19.bed2'  # 输入你的BED文件名称
files = {}  # 用于存储文件句柄的字典

for chunk in pd.read_csv(filename, sep='\t', header=None, chunksize=chunksize):
    grouped = chunk.groupby(3)
    for name, group in grouped:
        if name not in files:
            files[name] = open(f'/opt/shimw/G4TF/{name}.bed', 'w')
        group.iloc[:, :3].to_csv(files[name], sep='\t', header=False, index=False, mode='a')

# 记得关闭所有的文件句柄
for file in files.values():
    file.close()

# /home/shimw/software/bedToBigBed

import subprocess

for name in files:
    bed_file = f'{name}.bed'
    sorted_bed_file = f'{name}_sorted.bed'
    bigbed_file = f'{name}.bb'
    chrom_sizes_file = '/home/shimw/web/G4-portal/endoG4/static/hg19.chrom.sizes'  # change this to the path of your chromosome sizes file

    # construct the sort command and execute it
    sort_cmd = f'sort -k1,1 -k2,2n /opt/shimw/G4TF/{bed_file} > /opt/shimw/G4TF/{sorted_bed_file}'
    subprocess.run(sort_cmd, shell=True)

    # construct the bedToBigBed command and execute it
    bedtobigbed_cmd = f'/home/shimw/software/bedToBigBed /opt/shimw/G4TF/{sorted_bed_file} {chrom_sizes_file} /opt/shimw/G4TF/{bigbed_file}'
    subprocess.run(bedtobigbed_cmd, shell=True)