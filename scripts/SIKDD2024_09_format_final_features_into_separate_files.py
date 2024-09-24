features = open("statistically_significant_features_sorted_by_eta_squared.tsv", "r", encoding="UTF-8").readlines()

feature_ngrams_ACTUAL_GENERAL_NGRAMS = open("features_GENERAL_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_ACTUAL_STARTING_NGRAMS = open("features_STARTING_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_ACTUAL_ENDING_NGRAMS = open("features_ENDING_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_CVC_ROBUST_GENERAL_NGRAMS = open("features_CVC_ROBUST_GENERAL_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_CVC_FINEGRAINED_GENERAL_NGRAMS = open("features_CVC_FINEGRAINED_GENERAL_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_CVC_ROBUST_STARTING_NGRAMS = open("features_CVC_ROBUST_STARTING_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_CVC_FINEGRAINED_STARTING_NGRAMS = open("features_CVC_FINEGRAINED_STARTING_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_CVC_ROBUST_ENDING_NGRAMS = open("features_CVC_ROBUST_ENDING_NGRAMS.tsv", "w", encoding="UTF-8")
feature_ngrams_CVC_FINEGRAINED_ENDING_NGRAMS = open("features_CVC_FINEGRAINED_ENDING_NGRAMS.tsv", "w", encoding="UTF-8")




for file in [feature_ngrams_ACTUAL_GENERAL_NGRAMS,
             feature_ngrams_ACTUAL_STARTING_NGRAMS,
             feature_ngrams_ACTUAL_ENDING_NGRAMS,
             feature_ngrams_CVC_ROBUST_GENERAL_NGRAMS,
             feature_ngrams_CVC_FINEGRAINED_GENERAL_NGRAMS,
             feature_ngrams_CVC_ROBUST_STARTING_NGRAMS,
             feature_ngrams_CVC_FINEGRAINED_STARTING_NGRAMS,
             feature_ngrams_CVC_ROBUST_ENDING_NGRAMS,
             feature_ngrams_CVC_FINEGRAINED_ENDING_NGRAMS]:
    file.write("ngram\tngram_length\n")

# THESE FEATURES ARE NOT NGRAMS
non_ngram_features = ["percent_slovene_characters",
                      "fpos",
                      "placeholder_bigram",
                      "placeholder_trigram",
                      "placeholder_unigram",
                      "lexical_feature",
                      "pos",
                      "placeholder_bigram|END|",
                      "placeholder_trigram|END|",
                      "placeholder_unigram|END|",
                      "|BEG|placeholder_bigram",
                      "|BEG|placeholder_trigram",
                      "|BEG|placeholder_unigram"
                      ]


for line in features[1:]:  # SKIP HEADERS
    ngram_type,\
    feature_name,\
    k,\
    n,\
    Kruskal_Wallis_H_statistic,\
    p_value,\
    robust_p_value,\
    p_value_symbol,\
    eta_squared,\
    comparison_median,\
    group_1_median,\
    group_2_median,\
    comparison_average,\
    group_1_average,\
    group_2_average,\
    group_1_minimum,\
    group_2_minimum,\
    group_1_maximum,\
    group_2_maximum,\
    group_1_std,\
    group_2_std,\
    group_1_var,\
    group_2_var,\
    group_1_coefficient_of_variation,\
    group_2_coefficient_of_variation,\
    cumulative_percentage_of_total_eta_squared = line.strip("\n").split("\t")

    # SKIP NON-NGRAM FEATURES
    if feature_name in non_ngram_features:
        continue

    if ngram_type in ["GENERAL_NGRAMS_with_freq_1000plus","GENERAL_NGRAMS_with_freq_500-1000"]:
        #print("ACTUAL GENERAL NGRAMS", feature_name)
        feature_ngrams_ACTUAL_GENERAL_NGRAMS.write(f'{feature_name}\t{len(list(feature_name))}\n')

    elif ngram_type in ["ENDING_NGRAMS_with_freq_1000plus", "ENDING_NGRAMS_with_freq_500-1000"]:
        #print("ACTUAL ENDING NGRAMS", feature_name.split("|END|")[0])
        feature_ngrams_ACTUAL_ENDING_NGRAMS.write(f'{feature_name.split("|END|")[0]}\t{len(list(feature_name.split("|END|")[0]))}\n')

    elif ngram_type in ["STARTING_NGRAMS_with_freq_1000plus", "STARTING_NGRAMS_with_freq_500-1000"]:
        #print("ACTUAL STARTING NGRAMS", feature_name.split("|BEG|")[1])
        feature_ngrams_ACTUAL_STARTING_NGRAMS.write(f'{feature_name.split("|BEG|")[1]}\t{str(len(list(feature_name.split("|BEG|")[1])))}\n')

    elif ngram_type in ["CVC_FINEGRAINED_GENERAL_NGRAMS"]:
        #print("CVC FINEGRAINED GENERAL NGRAMS", feature_name)
        feature_ngrams_CVC_FINEGRAINED_GENERAL_NGRAMS.write(f"{feature_name}\t{len(list(feature_name))}\n")

    elif ngram_type in ["CVC_ROBUST_GENERAL_NGRAMS"]:
        #print("CVC ROBUST GENERAL NGRAMS", feature_name)
        feature_ngrams_CVC_ROBUST_GENERAL_NGRAMS.write(f"{feature_name}\t{len(list(feature_name))}\n")

    elif ngram_type in ["CVC_ROBUST_ENDING_NGRAMS"]:
        #print("CVC ROBUST ENDING NGRAMS", feature_name.split("|END|")[0])
        feature_ngrams_CVC_ROBUST_ENDING_NGRAMS.write(f'{feature_name.split("|END|")[0]}\t{len(list(feature_name.split("|END|")[0]))}\n')

    elif ngram_type in ["CVC_FINEGRAINED_ENDING_NGRAMS"]:
        #print("CVC FINEGRAINED ENDING NGRAMS", feature_name.split("|END|")[0])
        feature_ngrams_CVC_FINEGRAINED_ENDING_NGRAMS.write(f'{feature_name.split("|END|")[0]}\t{len(list(feature_name.split("|END|")[0]))}\n')

    elif ngram_type in ["CVC_FINEGRAINED_STARTING_NGRAMS"]:
        #print("CVC FINEGRAINED STARTING NGRAMS", feature_name.split("|BEG|")[1])
        feature_ngrams_CVC_FINEGRAINED_STARTING_NGRAMS.write(f'{feature_name.split("|BEG|")[1]}\t{len(list(feature_name.split("|BEG|")[1]))}\n')

    elif ngram_type in ["CVC_ROBUST_STARTING_NGRAMS"]:
        #print("CVC ROBUST STARTING NGRAMS", feature_name.split("|BEG|")[1])
        feature_ngrams_CVC_ROBUST_STARTING_NGRAMS.write(f'{feature_name.split("|BEG|")[1]}\t{len(list(feature_name.split("|BEG|")[1]))}\n')