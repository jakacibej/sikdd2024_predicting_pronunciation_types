from collections import defaultdict as dd

sep = " ~~~ "

# FUNCTION: GET FINEGRAINED POS FROM MSD
def get_finegrained_pos(msd):

    # RETURNS FINEGRAINED POS (TO DISCRIMINATE BETWEEN HOMONYMS)
    if msd.startswith("S"):
        finegrained_pos = msd[0:3]  # Som, Soz, Sos, Slz, Slm, Sls
    elif msd.startswith("P"):
        finegrained_pos = msd[0:2]  # Pd, Ps, Pp
    elif msd.startswith("R"):
        finegrained_pos = msd[0:2]  # Rs, Rd
    elif msd.startswith("G"):
        finegrained_pos = msd[0:3]  # Ggv, Ggn, Ggd
    elif msd.startswith("K"):
        finegrained_pos = msd[0:3]  # Kag, Kbg
    elif msd.startswith("Z"):
        finegrained_pos = msd[0:2]  # Zo, Zs, Zl
    elif msd.startswith("D"):
        finegrained_pos = msd[0:2]  # Dt, Dd
    elif msd.startswith("V"):
        finegrained_pos = msd[0:2]  # Vp, Vd
    elif msd.startswith(("L", "U", "O", "M")):
        finegrained_pos = msd[0:1]  # L, U, O, M
    elif msd.startswith("N"):
        finegrained_pos = msd[0:2]  # Nj, Np
    else:
        finegrained_pos = "NOT FOUND"

    return finegrained_pos



final_sloleks3_tsv = open("d:\\PycharmProjects\\PyBossa_agreement\\Sloleks3TSV_01_export_final_TSV_from_xml_split\\sloleks3.0_2023-10-21.tsv", "r", encoding="UTF-8").readlines()

#dict_lists_of_words_by_g2p_type_and_fpos = dd(list)

output = open("lemfpos_and_pronuncation_type.tsv", "w", encoding="UTF-8")
output.write("{}\n".format("\t".join([str(x) for x in ["sloleks_id", "lemma", "fpos", "pronunciation_type", "entry_status"]])))

set_of_already_covered_lemfpos = set()


for line in final_sloleks3_tsv[1:]:  # SKIP HEADERS
    sloleks_id,\
    sloleks_key,\
    lemma,\
    mte_msd_sl,\
    orthography_form,\
    dyn_acc_form_1,\
    dyn_acc_form_2,\
    dyn_acc_form_3,\
    dyn_acc_form_4,\
    ipa_pron_form_1,\
    ipa_pron_form_2,\
    ipa_pron_form_3,\
    ipa_pron_form_4,\
    sampa_pron_form_1,\
    sampa_pron_form_2,\
    sampa_pron_form_3,\
    sampa_pron_form_4,\
    orthography_norm_info,\
    orthography_gf2_rfreq,\
    entry_status,\
    pronunciation_type = line.strip("\n").split("\t")


    fpos = get_finegrained_pos(msd=mte_msd_sl)

    if not f"{sloleks_id}{sep}{fpos}{sep}{lemma}" in set_of_already_covered_lemfpos:
        set_of_already_covered_lemfpos.add(f"{sloleks_id}{sep}{fpos}{sep}{lemma}")
        output.write("{}\n".format("\t".join([str(x) for x in [sloleks_id, lemma, fpos, pronunciation_type, entry_status]])))


    #if not f"{fpos}{sep}{lemma}" in dict_lists_of_words_by_g2p_type_and_fpos[f"{fpos}{sep}{pronunciation_type}"]:
    #    dict_lists_of_words_by_g2p_type_and_fpos[f"{fpos}{sep}{pronunciation_type}"].append(f"{fpos}{sep}{lemma}")
    #    print(f"{fpos}{sep}{lemma}", pronunciation_type)


#for x in dict_lists_of_words_by_g2p_type_and_fpos:
#    print(x, dict_lists_of_words_by_g2p_type_and_fpos[x][:10], len(dict_lists_of_words_by_g2p_type_and_fpos[x]))