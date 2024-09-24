from collections import defaultdict as dd

sep = " ~~~ "

file_with_lemfpos = open("lemfpos_and_pronunciation_type_MANUAL_CORRECTIONS.tsv", "r", encoding="UTF-8").readlines()
dict_stats = dd(int)
dict_pronunciation_types = dd(int)
for line in file_with_lemfpos[1:]:  # SKIP HEADERS
    sloleks_id,\
    lemma,\
    fpos,\
    pronunciation_type,\
    entry_status = line.strip("\n").split("\t")

    identifier = f"{pronunciation_type}{sep}{fpos}{sep}{entry_status}"

    dict_stats[identifier] += 1
    dict_pronunciation_types[pronunciation_type] += 1

for x in sorted(dict_stats, key=lambda x:dict_stats[x], reverse=True):
    print(x, dict_stats[x])

#for x in sorted(dict_pronunciation_types, key=lambda x:dict_pronunciation_types[x], reverse=True):
    #print(x, dict_pronunciation_types[x])
#    print(f"|{x}|{dict_pronunciation_types[x]}|")