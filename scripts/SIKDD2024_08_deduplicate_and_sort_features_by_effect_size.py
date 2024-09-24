from collections import defaultdict as dd

file_with_all_features = open("ALL_FEATURES.tsv", "r", encoding="UTF-8").readlines()

deduplicated_lines = []
list_to_check_duplicates = []
for line in file_with_all_features[1:]:  # SKIP HEADERS
    # DEDUPLICATE LINES BASED ON ALL CELLS EXCEPT THE FIRST ONE (NGRAM_TYPE)
    if not "\t".join(line.strip("\n").split("\t")[1:]) in list_to_check_duplicates:
        list_to_check_duplicates.append("\t".join(line.strip("\n").split("\t")[1:]))
        deduplicated_lines.append(line)

dict_to_sort_deduplicated_lines = dd(list)

total_sum_of_eta_squared = 0.0

for line in deduplicated_lines:
    ngram_type,\
    feature_name, \
    k, \
    n, \
    Kruskal_Wallis_H_statistic, \
    p_value, \
    robust_p_value, \
    p_value_symbol, \
    eta_squared, \
    comparison_median, \
    group_1_median, \
    group_2_median, \
    comparison_average, \
    group_1_average, \
    group_2_average, \
    group_1_minimum, \
    group_2_minimum, \
    group_1_maximum, \
    group_2_maximum, \
    group_1_std, \
    group_2_std, \
    group_1_var, \
    group_2_var, \
    group_1_coefficient_of_variation, \
    group_2_coefficient_of_variation = line.strip("\n").split("\t")

    # FILTER OUT LINES THAT ARE NOT STATISTICALLY SIGNIFICANT
    if not p_value_symbol in ["ns", "_"]:
        dict_to_sort_deduplicated_lines[float(eta_squared)].append(line)
        total_sum_of_eta_squared += float(eta_squared)


# SORT LINES BY ETA SQUARED
output_with_sorted_relevant_features = open("statistically_significant_features_sorted_by_eta_squared.tsv", "w", encoding="UTF-8")
output_with_sorted_relevant_features.write("{}\n".format("\t".join([str(x) for x in ["ngram_type", "feature_name", "k", "n", "Kruskal_Wallis_H_statistic", "p_value", "robust_p_value", "p_value_symbol", "eta_squared", "comparison_median", "group_1_median", "group_2_median", "comparison_average", "group_1_average", "group_2_average", "group_1_minimum", "group_2_minimum", "group_1_maximum", "group_2_maximum", "group_1_std", "group_2_std", "group_1_var", "group_2_var", "group_1_coefficient_of_variation", "group_2_coefficient_of_variation", "cumulative_percentage_of_total_eta_squared"]])))

cumulative_percentage_of_total_eta_squared = 0.0
for key in sorted(dict_to_sort_deduplicated_lines, reverse=True):
    for a in dict_to_sort_deduplicated_lines[key]:
        #print(a.strip("\n"))
        individual_eta_squared = float(a.strip("\n").split("\t")[8])
        percentage_of_total_eta_squared = individual_eta_squared/total_sum_of_eta_squared*100
        cumulative_percentage_of_total_eta_squared += percentage_of_total_eta_squared
        print("{}\t{}".format(a.strip("\n"), str(cumulative_percentage_of_total_eta_squared)))
        output_with_sorted_relevant_features.write("{}\t{}\n".format(a.strip("\n"), str(cumulative_percentage_of_total_eta_squared)))