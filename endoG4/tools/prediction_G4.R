arg = commandArgs(T)
# library(pqsfinder, lib.loc = "/home/qians/R/x86_64-pc-linux-gnu-library/4.0/")
print(arg)
file_path = arg[1]
overlapping = arg[2]
max_length = as.numeric(arg[3])
min_score = as.numeric(arg[4])
max_bulge = as.numeric(arg[5])
max_mismatch = as.numeric(arg[6])
max_defect = as.numeric(arg[7])
min_loop = as.numeric(arg[8])
max_loop = as.numeric(arg[9])
min_run = as.numeric(arg[10])
max_run = as.numeric(arg[11])
print(overlapping)
if (overlapping=="False") {
  t_overlapping = FALSE
}else{
  t_overlapping = TRUE
}
genome <- readDNAStringSet(file_path)
dirname(file_path)
result_file = paste(dirname(file_path),"/",strsplit(basename(file_path),"\\.")[[1]][1],".txt",sep = "")
df = c()
for (n in 1:length(genome)) {
  pqs = pqsfinder::pqsfinder(genome[[n]],overlapping = t_overlapping,max_len = max_length,
                             min_score = min_score,run_min_len = min_run, run_max_len = max_run,
                             loop_min_len = min_loop, loop_max_len = max_loop, max_bulges = max_bulge,
                             max_mismatches = max_mismatch,max_defects = max_defect)
  pqs.df = data.frame(list(pqs@ranges,pqs@elementMetadata)) 
  pqs.df$chr = names(genome)[n]
  print(paste0(names(genome)[n]," done"))
  df = rbind(df,pqs.df)
}
print(result_file)
col = ncol(df)
df = df[,c(col,1:3,5,4,6:(col-1))]
df$ID = paste0("PQS",1:nrow(df))
data.table::fwrite(df,file = result_file,
       sep = '\t', row.names = FALSE, quote = FALSE)


