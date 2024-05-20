import argparse,os

def main(file):
    with open(file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            record = line.strip().split("\t")
            if record[2]!="gene":
                continue
            gene_info = record[8].split(";")
            gene_name = "NA"
            for i in gene_info:
                if i.strip().startswith("gene_id"):
                    gene_id = i.strip().replace("gene_id", "").replace('"', '').strip()
                    gene_id = gene_id.split(".")[0]
                if i.strip().startswith("gene_name"):
                    gene_name = i.strip().replace("gene_name", "").replace('"', '').strip()
                if i.strip().startswith("gene_biotype"):
                    gene_biotype = i.strip().replace("gene_biotype", "").replace('"', '').strip()
                if i.strip().startswith("gene_type"):
                    gene_biotype = i.strip().replace("gene_type", "").replace('"', '').strip()
            record[0] = f"chr{record[0]}"
            print(f"{record[0]}\t{record[3]}\t{record[4]}\t{record[6]}\t{gene_id}\t{gene_name}\t{gene_biotype}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="positional argument 1")
    args = parser.parse_args()
    main(args.file)