from collections import defaultdict as dd


def extract_starting_ngrams(string):
    dict_ngram_frequency = dd(int)
    length_of_string = len(list(string))
    # STARTING UNIGRAM
    dict_ngram_frequency[list(string)[0]] += 1
    # STARTING BIGRAM
    if length_of_string >= 2:
        dict_ngram_frequency["".join(list(string)[0:2])] += 1
    # STARTING TRIGRAM
    if length_of_string >= 3:
        dict_ngram_frequency["".join(list(string)[0:3])] += 1
    # STARTING 4-GRAM
    if length_of_string >= 4:
        dict_ngram_frequency["".join(list(string)[0:4])] += 1

    return dict_ngram_frequency



def extract_ending_ngrams(string):
    dict_ngram_frequency = dd(int)
    length_of_string = len(list(string))
    # ENDING UNIGRAM
    dict_ngram_frequency[list(string)[-1]] += 1
    # STARTING BIGRAM
    if length_of_string >= 2:
        dict_ngram_frequency["".join(list(string)[-2:])] += 1
    # STARTING TRIGRAM
    if length_of_string >= 3:
        dict_ngram_frequency["".join(list(string)[-3:])] += 1
    # STARTING 4-GRAM
    if length_of_string >= 4:
        dict_ngram_frequency["".join(list(string)[-4:])] += 1

    return dict_ngram_frequency



def extract_unigrams(string):
    dict_ngram_abs_frequency = dd(int)
    dict_ngram_rel_frequency = dd(float)
    total_number_of_ngrams_in_string = 0
    for character in list(string):
        dict_ngram_abs_frequency[character] += 1
        total_number_of_ngrams_in_string += 1

    for x in dict_ngram_abs_frequency:
        dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/total_number_of_ngrams_in_string

    return dict_ngram_abs_frequency, dict_ngram_rel_frequency


def extract_bigrams(string):
    dict_ngram_abs_frequency = dd(int)
    dict_ngram_rel_frequency = dd(float)
    total_number_of_ngrams_in_string = 0
    for index, character in enumerate(list(string)):
        try:
            character_1 = character
            character_2 = list(string)[index+1]
            bigram = f"{character_1}{character_2}"
            dict_ngram_abs_frequency[bigram] += 1
            total_number_of_ngrams_in_string += 1
        except:
            continue

    for x in dict_ngram_abs_frequency:
        dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/total_number_of_ngrams_in_string


    return dict_ngram_abs_frequency, dict_ngram_rel_frequency


def extract_trigrams(string):
    dict_ngram_abs_frequency = dd(int)
    dict_ngram_rel_frequency = dd(float)
    total_number_of_ngrams_in_string = 0
    for index, character in enumerate(list(string)):
        try:
            character_1 = character
            character_2 = list(string)[index + 1]
            character_3 = list(string)[index + 2]
            trigram = f"{character_1}{character_2}{character_3}"
            dict_ngram_abs_frequency[trigram] += 1
            total_number_of_ngrams_in_string += 1
        except:
            continue

    for x in dict_ngram_abs_frequency:
        dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/total_number_of_ngrams_in_string


    return dict_ngram_abs_frequency, dict_ngram_rel_frequency


def convert_to_CVC(string, conversion_dictionary):
    converted_characters = []
    for character in list(string):
        if character in conversion_dictionary:
            converted_characters.append(conversion_dictionary[character])
        else:
            converted_characters.append("-")

    return "".join(converted_characters)




"""
def extract_4_grams(string):
    dict_ngram_abs_frequency = dd(int)
    dict_ngram_rel_frequency = dd(float)
    total_number_of_ngrams_in_string = 0
    for index, character in enumerate(list(string)):
        try:
            character_1 = character
            character_2 = list(string)[index + 1]
            character_3 = list(string)[index + 2]
            character_4 = list(string)[index + 3]
            trigram = f"{character_1}{character_2}{character_3}{character_4}"
            dict_ngram_abs_frequency[trigram] += 1
            total_number_of_ngrams_in_string += 1
        except:
            continue

    for x in dict_ngram_abs_frequency:
        dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/total_number_of_ngrams_in_string


    return dict_ngram_abs_frequency, dict_ngram_rel_frequency
"""

file_with_pronunciation_types = open("lemfpos_and_pronunciation_type_MANUAL_CORRECTIONS.tsv", "r", encoding="UTF-8").readlines()

set_of_unigrams = set()
set_of_bigrams = set()
set_of_trigrams = set()
set_of_4grams = set()

set_of_unigrams_for_sloveneg2p = set()
set_of_unigrams_for_otherg2p = set()

output_with_unique_ngrams = open("unique_ngrams_CVC_ROBUST.tsv", "w", encoding="UTF-8")
output_with_unique_ngrams.write("{}\n".format("\t".join([str(x) for x in ["ngram", "frequency", "ngram_length"]])))

output_with_unique_ngrams_FINEGRAINED = open("unique_ngrams_CVC_FINEGRAINED.tsv", "w", encoding="UTF-8")
output_with_unique_ngrams_FINEGRAINED.write("{}\n".format("\t".join([str(x) for x in ["ngram", "frequency", "ngram_length"]])))


dict_unique_ngrams = dd(int)
dict_unique_ngrams_FINEGRAINED = dd(int)

CVC_ROBUST_dictionary = dd()
CVC_FINEGRAINED_dictionary = dd()
character_categorization = open("GF2.0_character_categorization.txt", "r", encoding="UTF-8").readlines()
for line in character_categorization[1:]:
    character_string, CV_ROBUST_category, CV_FINEGRAINED_category = line.strip("\n").split("\t")

    CVC_ROBUST_dictionary[character_string] = CV_ROBUST_category
    CVC_FINEGRAINED_dictionary[character_string] = CV_FINEGRAINED_category



for line in file_with_pronunciation_types[1:]:  # SKIP HEADERS
    sloleks_id,\
    lemma,\
    fpos,\
    pronunciation_type,\
    entry_status = line.strip("\n").split("\t")

    CVC_ROBUST_lemma = convert_to_CVC(string=lemma.lower(), conversion_dictionary=CVC_ROBUST_dictionary)

    CVC_FINEGRAINED_lemma = convert_to_CVC(string=lemma.lower(), conversion_dictionary=CVC_FINEGRAINED_dictionary)

    # EXTRACT UNIGRAMS FROM CVC ROBUST LEMMA
    unigrams_abs, unigrams_rel = extract_unigrams(string=CVC_ROBUST_lemma)
    for x in unigrams_abs:
        set_of_unigrams.add(x)
        dict_unique_ngrams[x] += 1

    # EXTRACT UNIGRAMS FROM CVC FINEGRAINED LEMMA
    unigrams_abs, unigrams_rel = extract_unigrams(string=CVC_FINEGRAINED_lemma)
    for x in unigrams_abs:
        set_of_unigrams.add(x)
        dict_unique_ngrams_FINEGRAINED[x] += 1

    # EXTRACT BIGRAMS FROM CVC ROBUST LEMMA
    bigrams_abs, bigrams_rel = extract_bigrams(string=CVC_ROBUST_lemma)
    for x in bigrams_abs:
        set_of_bigrams.add(x)
        dict_unique_ngrams[x] += 1

    # EXTRACT BIGRAMS FROM CVC FINEGRAINED LEMMA
    bigrams_abs, bigrams_rel = extract_bigrams(string=CVC_FINEGRAINED_lemma)
    for x in bigrams_abs:
        set_of_bigrams.add(x)
        dict_unique_ngrams_FINEGRAINED[x] += 1


    # EXTRACT TRIGRAMS FROM CVC ROBUST LEMMA
    trigrams_abs, trigrams_rel = extract_trigrams(string=CVC_ROBUST_lemma)
    for x in trigrams_abs:
        set_of_trigrams.add(x)
        dict_unique_ngrams[x] += 1

    # EXTRACT TRIGRAMS FROM CVC FINEGRAINED LEMMA
    trigrams_abs, trigrams_rel = extract_trigrams(string=CVC_FINEGRAINED_lemma)
    for x in trigrams_abs:
        set_of_trigrams.add(x)
        dict_unique_ngrams_FINEGRAINED[x] += 1


    # EXTRACT 4-GRAMS
    #fourgrams_abs, fourgrams_rel = extract_4_grams(string=lemma)
    #for x in fourgrams_abs:
    #    set_of_4grams.add(x)


#print(set_of_unigrams)
#print(set_of_bigrams)
#print(len(set_of_trigrams))
#print(len(set_of_4grams))

print("SLOVENE G2P CHARACTERS:", set_of_unigrams_for_sloveneg2p)
print("OTHER G2P CHARACTERS:", set_of_unigrams_for_otherg2p)
print("UNIQUELY SLOVENE G2P CHARACTERS:", set_of_unigrams_for_sloveneg2p-set_of_unigrams_for_otherg2p)
print("UNIQUELY OTHER G2P CHARACTERS:", set_of_unigrams_for_otherg2p-set_of_unigrams_for_sloveneg2p)

for x in sorted(dict_unique_ngrams, key=lambda x: dict_unique_ngrams[x], reverse=True):
    print(x, dict_unique_ngrams[x])
    length_of_ngram = len(list(x))
    output_with_unique_ngrams.write("{}\n".format("\t".join([str(x) for x in [x, dict_unique_ngrams[x], length_of_ngram]])))

for x in sorted(dict_unique_ngrams_FINEGRAINED, key=lambda x: dict_unique_ngrams_FINEGRAINED[x], reverse=True):
    print(x, dict_unique_ngrams_FINEGRAINED[x])
    length_of_ngram = len(list(x))
    output_with_unique_ngrams_FINEGRAINED.write("{}\n".format("\t".join([str(x) for x in [x, dict_unique_ngrams_FINEGRAINED[x], length_of_ngram]])))

