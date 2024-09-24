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


# TODO - GET PERCENTAGE OF SLOVENE VS. NON-SLOVENE CHARACTERS

# TODO - GET MORPHOSYNTACTIC FEATURES

#print(extract_starting_ngrams("abeceda"))
#print(extract_starting_ngrams("ab"))
#print(extract_ending_ngrams(string="abeceda"))
#print(extract_ending_ngrams(string="ca"))
#print(extract_bigrams(string="bethesda"))
#print(extract_bigrams(string="ba"))
#print(extract_trigrams(string="bethesda"))
#print(extract_4_grams(string="bethesda"))
#print(extract_bigrams(string="adarkad"))
#print(extract_unigrams(string="adarkad"))

file_with_pronunciation_types = open("lemfpos_and_pronunciation_type_MANUAL_CORRECTIONS.tsv", "r", encoding="UTF-8").readlines()

set_of_unigrams = set()
set_of_bigrams = set()
set_of_trigrams = set()
set_of_4grams = set()

set_of_unigrams_for_sloveneg2p = set()
set_of_unigrams_for_otherg2p = set()

output_with_unique_ngrams = open("unique_ngrams.tsv", "w", encoding="UTF-8")
output_with_unique_ngrams.write("{}\n".format("\t".join([str(x) for x in ["ngram", "frequency", "ngram_length"]])))

dict_unique_ngrams = dd(int)

for line in file_with_pronunciation_types[1:]:  # SKIP HEADERS
    sloleks_id,\
    lemma,\
    fpos,\
    pronunciation_type,\
    entry_status = line.strip("\n").split("\t")

    #if any([x in lemma for x in ["y", "w"]]) and pronunciation_type in ["Slovene G2P", "Slovene G2P with minor deviation"]:
    #    print(lemma, fpos)

    #if any([x in lemma for x in ["š", "č"]]) and pronunciation_type in ["Other G2P"]:
    #    print(lemma, fpos)

    # EXTRACT UNIGRAMS
    unigrams_abs, unigrams_rel = extract_unigrams(string=lemma.lower())
    for x in unigrams_abs:
        set_of_unigrams.add(x)
        dict_unique_ngrams[x] += 1
        # GET UNIGRAMS FOR SLOVENE G2P
        if pronunciation_type in ["Slovene G2P", "Slovene G2P with minor deviation"]:
            set_of_unigrams_for_sloveneg2p.add(x)
        if pronunciation_type in ["Other G2P"]:
            set_of_unigrams_for_otherg2p.add(x)

    # EXTRACT BIGRAMS
    bigrams_abs, bigrams_rel = extract_bigrams(string=lemma.lower())
    for x in bigrams_abs:
        set_of_bigrams.add(x)
        dict_unique_ngrams[x] += 1

    # EXTRACT TRIGRAMS
    trigrams_abs, trigrams_rel = extract_trigrams(string=lemma.lower())
    for x in trigrams_abs:
        set_of_trigrams.add(x)
        dict_unique_ngrams[x] += 1

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

