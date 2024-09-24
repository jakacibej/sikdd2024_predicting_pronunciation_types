from collections import defaultdict as dd

dict_pos_to_float = {"S":1.0,
                     "P":2.0,
                     "R":3.0,
                     "G":4.0}

dict_lexical_features_to_float = {"Sl":1.0,
                                  "So":2.0,
                                  "Pp":3.0,
                                  "Pd":4.0,
                                  "Ps":5.0,
                                  "Rs":6.0,
                                  "Rd":7.0,
                                  "Gg":8.0}

dict_fpos_to_float = {"Slm":0.0,
                      "Slz":1.0,
                      "Sls":2.0,
                      "Som":3.0,
                      "Soz":4.0,
                      "Sos":5.0,
                      "Ps":6.0,
                      "Pp":7.0,
                      "Pd":8.0,
                      "Rs":9.0,
                      "Rd":10.0,
                      "Ggn":11.0,
                      "Ggd":12.0,
                      "Ggv":13.0}

slovene_characters = {"a", "b", "c", "č", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "š", "t", "u", "v", "z", "ž", "đ", "ć"}

# TODO - GET PERCENTAGE OF SLOVENE VS. NON-SLOVENE CHARACTERS
def get_percentage_of_slovene_characters_in_lemma(string, set_of_slovene_characters):
    count_slovene_characters = 0
    for character in list(string):
        if character in set_of_slovene_characters:
            count_slovene_characters += 1

    return count_slovene_characters/len(list(string))


def get_number_of_ngrams_within_lemma(string):
    # GET NUMBER OF UNIGRAMS
    nr_unigrams = len(list(string))
    # GET NUMBER OF BIGRAMS
    nr_bigrams = 0
    for index, character in enumerate(list(string)):
        try:
            character_1 = character
            character_2 = list(string)[index+1]
            nr_bigrams += 1
        except:
            continue
    # GET NUMBER OF TRIGRAMS
    nr_trigrams = 0
    for index, character in enumerate(list(string)):
        try:
            character_1 = character
            character_2 = list(string)[index+1]
            character_3 = list(string)[index+2]
            nr_trigrams += 1
        except:
            continue

    return nr_unigrams, nr_bigrams, nr_trigrams


def extract_starting_ngrams(string):
    dict_ngram_abs_frequency = dd(int)
    dict_ngram_rel_frequency = dd(float)
    nr_unigrams, nr_bigrams, nr_trigrams = get_number_of_ngrams_within_lemma(string=string)

    length_of_string = len(list(string))
    # STARTING UNIGRAM
    dict_ngram_abs_frequency[list(string)[0]] += 1
    # STARTING BIGRAM
    if length_of_string >= 2:
        dict_ngram_abs_frequency["".join(list(string)[0:2])] += 1
    # STARTING TRIGRAM
    if length_of_string >= 3:
        dict_ngram_abs_frequency["".join(list(string)[0:3])] += 1
    # STARTING 4-GRAM
    #if length_of_string >= 4:
    #    dict_ngram_abs_frequency["".join(list(string)[0:4])] += 1

    for x in dict_ngram_abs_frequency:
        if len(list(x)) == 1:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/nr_unigrams
        elif len(list(x)) == 2:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/nr_bigrams
        elif len(list(x)) == 3:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/nr_trigrams

    return dict_ngram_abs_frequency, dict_ngram_rel_frequency



def extract_ending_ngrams(string):
    dict_ngram_abs_frequency = dd(int)
    dict_ngram_rel_frequency = dd(float)
    nr_unigrams, nr_bigrams, nr_trigrams = get_number_of_ngrams_within_lemma(string=string)
    length_of_string = len(list(string))

    # ENDING UNIGRAM
    dict_ngram_abs_frequency[list(string)[-1]] += 1
    # STARTING BIGRAM
    if length_of_string >= 2:
        dict_ngram_abs_frequency["".join(list(string)[-2:])] += 1
    # STARTING TRIGRAM
    if length_of_string >= 3:
        dict_ngram_abs_frequency["".join(list(string)[-3:])] += 1
    # STARTING 4-GRAM
    #if length_of_string >= 4:
    #    dict_ngram_frequency["".join(list(string)[-4:])] += 1

    for x in dict_ngram_abs_frequency:
        if len(list(x)) == 1:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/nr_unigrams
        elif len(list(x)) == 2:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/nr_bigrams
        elif len(list(x)) == 3:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x]/nr_trigrams

    return dict_ngram_abs_frequency, dict_ngram_rel_frequency



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



def convert_to_CVC(string, conversion_dictionary):
    converted_characters = []
    for character in list(string):
        if character in conversion_dictionary:
            converted_characters.append(conversion_dictionary[character])
        else:
            converted_characters.append("-")

    return "".join(converted_characters)




def vectorize_lemfpos(lemma, fpos, list_of_unique_ngrams_for_vectorization, get_general_ngrams, get_starting_ngrams, get_ending_ngrams):
    frequency_dictionary_of_general_ngrams_in_lemma = dd(float)

    frequency_dictionary_of_ending_ngrams_in_lemma = dd(float)

    frequency_dictionary_of_starting_ngrams_in_lemma = dd(float)

    # POPULATE DICTIONARIES WITH ALL UNIQUE NGRAMS
    for unique_ngram in list_of_unique_ngrams_for_vectorization:
        frequency_dictionary_of_general_ngrams_in_lemma[unique_ngram] = 0.0
        frequency_dictionary_of_ending_ngrams_in_lemma[unique_ngram] = 0.0
        frequency_dictionary_of_starting_ngrams_in_lemma[unique_ngram] = 0.0
    # + A PLACEHOLDER NGRAM FOR ALL OTHER POTENTIAL NGRAMS NOT SEEN IN THIS INITIAL BATCH
    frequency_dictionary_of_general_ngrams_in_lemma['placeholder_unigram'] = 0.0
    frequency_dictionary_of_starting_ngrams_in_lemma['placeholder_unigram'] = 0.0
    frequency_dictionary_of_ending_ngrams_in_lemma['placeholder_unigram'] = 0.0
    frequency_dictionary_of_general_ngrams_in_lemma['placeholder_bigram'] = 0.0
    frequency_dictionary_of_starting_ngrams_in_lemma['placeholder_bigram'] = 0.0
    frequency_dictionary_of_ending_ngrams_in_lemma['placeholder_bigram'] = 0.0
    frequency_dictionary_of_general_ngrams_in_lemma['placeholder_trigram'] = 0.0
    frequency_dictionary_of_starting_ngrams_in_lemma['placeholder_trigram'] = 0.0
    frequency_dictionary_of_ending_ngrams_in_lemma['placeholder_trigram'] = 0.0

    # GET FEATURES BASED ON MORPHOSYNTACTIC TAGS
    pos_feature = dict_pos_to_float[fpos[0]]
    lexical_feature = dict_lexical_features_to_float[fpos[0:2]]
    fpos_feature = dict_fpos_to_float[fpos]

    # GET FEATURE BASED ON SLOVENE CHARACTERS
    percentage_of_slovene_characters = get_percentage_of_slovene_characters_in_lemma(string=lemma, set_of_slovene_characters=slovene_characters)

    if get_general_ngrams:
        # EXTRACT UNIGRAMS FROM LEMMA
        unigrams_dict_abs, unigrams_dict_rel = extract_unigrams(string=lemma)

        for unigram in unigrams_dict_rel:
            if unigram in frequency_dictionary_of_general_ngrams_in_lemma:
                frequency_dictionary_of_general_ngrams_in_lemma[unigram] += unigrams_dict_rel[unigram]
            else:
                frequency_dictionary_of_general_ngrams_in_lemma['placeholder_unigram'] += unigrams_dict_rel[unigram]

        # EXTRACT BIGRAMS FROM LEMMA
        bigrams_dict_abs, bigrams_dict_rel = extract_bigrams(string=lemma)

        for bigram in bigrams_dict_rel:
            if bigram in frequency_dictionary_of_general_ngrams_in_lemma:
                frequency_dictionary_of_general_ngrams_in_lemma[bigram] += bigrams_dict_rel[bigram]
            else:
                frequency_dictionary_of_general_ngrams_in_lemma['placeholder_bigram'] += bigrams_dict_rel[bigram]

        # EXTRACT TRIGRAMS FROM LEMMA
        trigrams_dict_abs, trigrams_dict_rel = extract_trigrams(string=lemma)

        for trigram in trigrams_dict_rel:
            if trigram in frequency_dictionary_of_general_ngrams_in_lemma:
                frequency_dictionary_of_general_ngrams_in_lemma[trigram] += trigrams_dict_rel[trigram]
            else:
                frequency_dictionary_of_general_ngrams_in_lemma['placeholder_trigram'] += trigrams_dict_rel[trigram]

    if get_ending_ngrams:
        # EXTRACT ENDING NGRAMS FROM LEMMA
        ending_ngrams_abs, ending_ngrams_rel = extract_ending_ngrams(string=lemma)

        for ending_ngram in ending_ngrams_rel:
            if ending_ngram in frequency_dictionary_of_ending_ngrams_in_lemma:
                frequency_dictionary_of_ending_ngrams_in_lemma[ending_ngram] += ending_ngrams_rel[ending_ngram]
            else:
                if len(list(ending_ngram)) == 1:
                    frequency_dictionary_of_ending_ngrams_in_lemma['placeholder_unigram'] += ending_ngrams_rel[ending_ngram]
                elif len(list(ending_ngram)) == 2:
                    frequency_dictionary_of_ending_ngrams_in_lemma['placeholder_bigram'] += ending_ngrams_rel[ending_ngram]
                elif len(list(ending_ngram)) == 3:
                    frequency_dictionary_of_ending_ngrams_in_lemma['placeholder_trigram'] += ending_ngrams_rel[ending_ngram]

    if get_starting_ngrams:
        # EXTRACT STARTING NGRAMS FROM LEMMA
        starting_ngrams_abs, starting_ngrams_rel = extract_starting_ngrams(string=lemma)

        for starting_ngram in starting_ngrams_rel:
            if starting_ngram in frequency_dictionary_of_starting_ngrams_in_lemma:
                frequency_dictionary_of_starting_ngrams_in_lemma[starting_ngram] = starting_ngrams_rel[starting_ngram]
            else:
                if len(list(starting_ngram)) == 1:
                    frequency_dictionary_of_starting_ngrams_in_lemma['placeholder_unigram'] = starting_ngrams_rel[starting_ngram]
                elif len(list(starting_ngram)) == 2:
                    frequency_dictionary_of_starting_ngrams_in_lemma['placeholder_bigram'] = starting_ngrams_rel[starting_ngram]
                elif len(list(starting_ngram)) == 3:
                    frequency_dictionary_of_starting_ngrams_in_lemma['placeholder_trigram'] = starting_ngrams_rel[starting_ngram]

    list_of_feature_names = []
    list_of_feature_names.append("pos")
    list_of_feature_names.append("lexical_feature")
    list_of_feature_names.append("fpos")
    list_of_feature_names.append("percent_slovene_characters")

    if get_general_ngrams:
        # ADD NGRAMS IN GENERAL
        for ngram in frequency_dictionary_of_general_ngrams_in_lemma:
            list_of_feature_names.append(ngram)

    if get_ending_ngrams:
        # ADD NAMES OF ENDING NGRAMS
        for ngram in frequency_dictionary_of_ending_ngrams_in_lemma:
            list_of_feature_names.append(f"{ngram}|END|")

    if get_starting_ngrams:
        # ADD NAMES OF STARTING NGRAMS
        for ngram in frequency_dictionary_of_starting_ngrams_in_lemma:
            list_of_feature_names.append(f"|BEG|{ngram}")

    list_of_features = []
    list_of_features.append(pos_feature)
    list_of_features.append(lexical_feature)
    list_of_features.append(fpos_feature)
    list_of_features.append(percentage_of_slovene_characters)

    if get_general_ngrams:
        # ADD FREQUENCIES OF NGRAMS IN GENERAL
        for ngram in frequency_dictionary_of_general_ngrams_in_lemma:
            list_of_features.append(frequency_dictionary_of_general_ngrams_in_lemma[ngram])

    if get_ending_ngrams:
        # ADD FREQUENCIES OF ENDING NGRAMS
        for ngram in frequency_dictionary_of_ending_ngrams_in_lemma:
            list_of_features.append(frequency_dictionary_of_ending_ngrams_in_lemma[ngram])

    if get_starting_ngrams:
        # ADD FREQUENCIES OF STARTING NGRAMS
        for ngram in frequency_dictionary_of_starting_ngrams_in_lemma:
            list_of_features.append(frequency_dictionary_of_starting_ngrams_in_lemma[ngram])

    return list_of_features, list_of_feature_names



file_with_pronunciation_types = open("lemfpos_and_pronunciation_type_MANUAL_CORRECTIONS.tsv", "r", encoding="UTF-8").readlines()

# DETERMINE WHICH NGRAMS YOU ARE EXTRACTING
are_you_getting_general_ngrams = False
are_you_getting_ending_ngrams = False
#are_you_getting_ending_ngrams = True
are_you_getting_starting_ngrams = True
#are_you_getting_starting_ngrams = False

#unique_ngrams = [line.strip("\n").split("\t")[0] for line in open("unique_ngrams_ENTIRE_SLOLEKS3.tsv", "r", encoding="UTF-8").readlines()[1:]]
#unique_ngrams = [line.strip("\n").split("\t")[0] for line in open("unique_ngrams_ENTIRE_SLOLEKS3.tsv", "r", encoding="UTF-8").readlines()[1:] if int(line.strip("\n").split("\t")[1]) >= 1000]

# ROBUST CVC NGRAMS
#unique_ngrams = [line.strip("\n").split("\t")[0] for line in open("unique_ngrams_CVC_ROBUST.tsv", "r", encoding="UTF-8").readlines()[1:]]

# FINEGRAINED CVC NGRAMS
unique_ngrams = [line.strip("\n").split("\t")[0] for line in open("unique_ngrams_CVC_FINEGRAINED.tsv", "r", encoding="UTF-8").readlines()[1:]]

output_with_features_for_analysis = open("features_for_analysis.tsv", "w", encoding="UTF-8")

only_write_feature_names_once = True

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

    # ONLY TAKE RELEVANT FPOS AND PRONUNCIATION TYPES INTO ACCOUNT
    if fpos in dict_fpos_to_float and pronunciation_type in ["Slovene G2P", "Slovene G2P with minor deviation", "Other G2P"]:

        #features, feature_names = vectorize_lemfpos(lemma=CVC_ROBUST_lemma, fpos=fpos, list_of_unique_ngrams_for_vectorization=unique_ngrams, get_general_ngrams=are_you_getting_general_ngrams, get_ending_ngrams=are_you_getting_ending_ngrams, get_starting_ngrams=are_you_getting_starting_ngrams)
        features, feature_names = vectorize_lemfpos(lemma=CVC_FINEGRAINED_lemma, fpos=fpos, list_of_unique_ngrams_for_vectorization=unique_ngrams, get_general_ngrams=are_you_getting_general_ngrams, get_ending_ngrams=are_you_getting_ending_ngrams, get_starting_ngrams=are_you_getting_starting_ngrams)


        if only_write_feature_names_once:
            output_with_features_for_analysis.write("{}\n".format("\t".join([str(x) for x in ["pronunciation_type", "sloleks_id", "lemma", "fpos", "\t".join(feature_names)]])))
            only_write_feature_names_once = False

        #print(pronunciation_type, sloleks_id, lemma, fpos, len(features), features[0:10], feature_names[0:10])

        output_with_features_for_analysis.write("{}\n".format("\t".join([str(x) for x in [pronunciation_type, sloleks_id, lemma, fpos, "\t".join([str(x) for x in features])]])))