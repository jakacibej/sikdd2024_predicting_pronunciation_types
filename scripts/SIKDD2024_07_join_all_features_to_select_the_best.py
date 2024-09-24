files_with_features = [("kruskal_wallis_test_results_FREQ_1000plus_GENERAL-NGRAMS.tsv", "GENERAL_NGRAMS_with_freq_1000plus"),
                       ("kruskal_wallis_test_results_FREQ_1000plus_ENDING-NGRAMS.tsv", "ENDING_NGRAMS_with_freq_1000plus"),
                       ("kruskal_wallis_test_results_FREQ_1000plus_STARTING-NGRAMS.tsv", "STARTING_NGRAMS_with_freq_1000plus"),
                       ("kruskal_wallis_test_results_CVC_ROBUST_GENERAL_NGRAMS.tsv", "CVC_ROBUST_GENERAL_NGRAMS"),
                       ("kruskal_wallis_test_results_CVC_ROBUST_ENDING-NGRAMS.tsv", "CVC_ROBUST_ENDING_NGRAMS"),
                       ("kruskal_wallis_test_results_CVC_ROBUST_STARTING-NGRAMS.tsv", "CVC_ROBUST_STARTING_NGRAMS"),
                       ("kruskal_wallis_test_results_CVC_FINEGRAINED_GENERAL-NGRAMS.tsv", "CVC_FINEGRAINED_GENERAL_NGRAMS"),
                       ("kruskal_wallis_test_results_CVC_FINEGRAINED_ENDING-NGRAMS.tsv", "CVC_FINEGRAINED_ENDING_NGRAMS"),
                       ("kruskal_wallis_test_results_CVC_FINEGRAINED_STARTING-NGRAMS.tsv", "CVC_FINEGRAINED_STARTING_NGRAMS"),
                       ("kruskal_wallis_test_results_FREQ500-1000_STARTING-NGRAMS.tsv", "STARTING_NGRAMS_with_freq_500-1000"),
                       ("kruskal_wallis_test_results_FREQ500-1000_ENDING-NGRAMS.tsv", "ENDING_NGRAMS_with_freq_500-1000"),
                       ("kruskal_wallis_test_results_FREQ500-1000_GENERAL-NGRAMS.tsv", "GENERAL_NGRAMS_with_freq_500-1000")]


output_all_features = open("ALL_FEATURES.tsv", "w", encoding="UTF-8")
output_all_features.write("{}\n".format("\t".join([str(x) for x in ["ngram_type", "feature_name", "k", "n", "Kruskal_Wallis_H_statistic", "p_value", "robust_p_value", "p_value_symbol", "eta_squared", "comparison_median", "group_1_median", "group_2_median", "comparison_average", "group_1_average", "group_2_average", "group_1_minimum", "group_2_minimum", "group_1_maximum", "group_2_maximum", "group_1_std", "group_2_std", "group_1_var", "group_2_var", "group_1_coefficient_of_variation", "group_2_coefficient_of_variation"]])))
for path, ngram_type in files_with_features:
    read_file = open(path, "r", encoding="UTF-8").readlines()
    for line in read_file[1:]:  # SKIP HEADERS
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
        group_2_coefficient_of_variation = line.strip("\n").split("\t")

        output_all_features.write("{}\n".format("\t".join([str(x) for x in [ngram_type, feature_name, k, n, Kruskal_Wallis_H_statistic, p_value, robust_p_value, p_value_symbol, eta_squared, comparison_median, group_1_median, group_2_median, comparison_average, group_1_average, group_2_average, group_1_minimum, group_2_minimum, group_1_maximum, group_2_maximum, group_1_std, group_2_std, group_1_var, group_2_var, group_1_coefficient_of_variation, group_2_coefficient_of_variation]])))