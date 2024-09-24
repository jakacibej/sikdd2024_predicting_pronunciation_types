from scipy import stats
import numpy as np
from collections import defaultdict as dd

def perform_kruskal_wallis_test(list_of_values_1, list_of_values_2):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html

    Kruskal_Wallis_H_statistic, p_value = stats.kruskal(list_of_values_1, list_of_values_2)

    """
    # https://www.graphpad.com/support/faq/what-is-the-meaning-of--or--or--in-reports-of-statistical-significance-from-prism-or-instat/
    Symbol Meaning
    ns P > 0.05
    * P ≤ 0.05
    ** P ≤ 0.01
    *** P ≤ 0.001
    **** P ≤ 0.0001 (For the last two choices only)
    """

    if p_value <= 0.0001:
        robust_p_value = "p ≤ 0.0001"
        p_value_symbol = "****"
    elif p_value <= 0.001:
        robust_p_value = "p ≤ 0.001"
        p_value_symbol = "***"
    elif p_value <= 0.01:
        robust_p_value = "p ≤ 0.01"
        p_value_symbol = "**"
    elif p_value <= 0.05:
        robust_p_value = "p ≤ 0.05"
        p_value_symbol = "*"
    elif p_value > 0.05:
        robust_p_value = "p > 0.05"
        p_value_symbol = "ns"
    else:
        robust_p_value = "?"
        p_value_symbol = "?"

    group_1_average = np.average(list_of_values_1)
    group_2_average = np.average(list_of_values_2)

    # COMPARE AVERAGES
    if group_1_average > group_2_average:
        comparison_average = "µ₁ > µ₂"
    elif group_1_average < group_2_average:
        comparison_average = "µ₁ < µ₂"
    else:
        comparison_average = "µ₁ = µ₂"

    group_1_median = np.median(list_of_values_1)
    group_2_median = np.median(list_of_values_2)

    if group_1_median > group_2_median:
        comparison_median = "M₁ > M₂"
    elif group_1_median < group_2_median:
        comparison_median = "M₁ < M₂"
    else:
        comparison_median = "M₁ = M₂"

    group_1_minimum = np.min(list_of_values_1)
    group_2_minimum = np.min(list_of_values_2)

    group_1_maximum = np.max(list_of_values_1)
    group_2_maximum = np.max(list_of_values_2)

    group_1_std = np.std(list_of_values_1)
    group_2_std = np.std(list_of_values_2)

    group_1_var = np.var(list_of_values_1)
    group_2_var = np.var(list_of_values_2)

    group_1_coefficient_of_variation = group_1_std / group_1_average  # https://stackoverflow.com/questions/42754627/coefficient-of-variation-and-numpy
    group_2_coefficient_of_variation = group_2_std / group_2_average

    k = 2  # WE COMPARE TWO GROUPS, SO k = 2
    n = len(list_of_values_1) + len(list_of_values_2)  # NUMBER OF ALL OBSERVATIONS

    # EFFECT SIZE
    # https://rpkgs.datanovia.com/rstatix/reference/kruskal_effsize.html
    # eta2[H] = (H - k + 1)/(n - k); where H is the value obtained in the Kruskal-Wallis test; k is the number of groups; n is the total number of observations.
    # The eta-squared estimate assumes values from 0 to 1 and multiplied by 100 indicates the percentage of variance in the dependent variable explained by the independent variable. The interpretation values commonly in published litterature are: 0.01- < 0.06 (small effect), 0.06 - < 0.14 (moderate effect) and >= 0.14 (large effect).

    eta_squared = (Kruskal_Wallis_H_statistic - k + 1) / (n - k)

    return k, n, Kruskal_Wallis_H_statistic, p_value, robust_p_value, p_value_symbol, eta_squared, comparison_median, group_1_median, group_2_median, comparison_average, group_1_average, group_2_average, group_1_minimum, group_2_minimum, group_1_maximum, group_2_maximum, group_1_std, group_2_std, group_1_var, group_2_var, group_1_coefficient_of_variation, group_2_coefficient_of_variation


#file_with_features = open("features_for_analysis_FREQ_1000plus_GENERAL-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_FREQ_1000plus_ENDING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_FREQ_1000plus_STARTING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_CVC_ROBUST_GENERAL-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_CVC_FINEGRAINED_GENERAL-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_CVC_ROBUST_ENDING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_CVC_FINEGRAINED_ENDING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_CVC_ROBUST_STARTING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
file_with_features = open("features_for_analysis_CVC_FINEGRAINED_STARTING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_FREQ500-1000_GENERAL-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_FREQ500-1000_ENDING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()
#file_with_features = open("features_for_analysis_FREQ500-1000_STARTING-NGRAMS.tsv", "r", encoding="UTF-8").readlines()


feature_names = file_with_features[0].strip("\n").split("\t")[4:]

output = open("kruskal_wallis_test_results.tsv", "w", encoding="UTF-8")
output.write("{}\n".format("\t".join([str(x) for x in ["feature_name", "k", "n", "Kruskal_Wallis_H_statistic", "p_value", "robust_p_value", "p_value_symbol", "eta_squared", "comparison_median", "group_1_median", "group_2_median", "comparison_average", "group_1_average", "group_2_average", "group_1_minimum", "group_2_minimum", "group_1_maximum", "group_2_maximum", "group_1_std", "group_2_std", "group_1_var", "group_2_var", "group_1_coefficient_of_variation", "group_2_coefficient_of_variation"]])))

for index, feature_name in enumerate(feature_names):
    dict_features = dd(list)
    for line in file_with_features[1:]:  # SKIP HEADERS
        pronunciation_type, sloleks_id, lemma, fpos = line.strip("\n").split("\t")[0:4]
        features = line.strip("\n").split("\t")[4:]

        if pronunciation_type in ["Slovene G2P", "Slovene G2P with minor deviation"]:
            pronunciation_type = "Slovene G2P"

        dict_features[pronunciation_type].append(float(features[index]))

    try:
        k, n, Kruskal_Wallis_H_statistic, p_value, robust_p_value, p_value_symbol, eta_squared, comparison_median, group_1_median, group_2_median, comparison_average, group_1_average, group_2_average, group_1_minimum, group_2_minimum, group_1_maximum, group_2_maximum, group_1_std, group_2_std, group_1_var, group_2_var, group_1_coefficient_of_variation, group_2_coefficient_of_variation = perform_kruskal_wallis_test(list_of_values_1=dict_features["Slovene G2P"], list_of_values_2=dict_features["Other G2P"])
    except:
        k = n = Kruskal_Wallis_H_statistic = p_value = robust_p_value = p_value_symbol = eta_squared = comparison_median = group_1_median = group_2_median = comparison_average = group_1_average = group_2_average = group_1_minimum = group_2_minimum = group_1_maximum = group_2_maximum = group_1_std = group_2_std = group_1_var = group_2_var = group_1_coefficient_of_variation = group_2_coefficient_of_variation = "_"

    print(feature_name, k, n, Kruskal_Wallis_H_statistic, p_value, robust_p_value, p_value_symbol, eta_squared, comparison_median, group_1_median, group_2_median, comparison_average, group_1_average, group_2_average, group_1_minimum, group_2_minimum, group_1_maximum, group_2_maximum, group_1_std, group_2_std, group_1_var, group_2_var, group_1_coefficient_of_variation, group_2_coefficient_of_variation)
    output.write("{}\n".format("\t".join([str(x) for x in [feature_name, k, n, Kruskal_Wallis_H_statistic, p_value, robust_p_value, p_value_symbol, eta_squared, comparison_median, group_1_median, group_2_median, comparison_average, group_1_average, group_2_average, group_1_minimum, group_2_minimum, group_1_maximum, group_2_maximum, group_1_std, group_2_std, group_1_var, group_2_var, group_1_coefficient_of_variation, group_2_coefficient_of_variation]])))