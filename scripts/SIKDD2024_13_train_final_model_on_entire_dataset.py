from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import os
from collections import defaultdict as dd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import dummy
import numpy as np
from sklearn.model_selection import cross_val_score
import random
from sklearn import preprocessing
import pickle



sep = " ~~~ "

class Vectorizer:

    def __init__(self, resources_directory):

        # DICTIONARIES TO CONVERT MORPHOSYNTACTIC FEATURES TO FLOATS
        self.dict_pos_to_float = {"S": 1.0,
                             "P": 2.0,
                             "R": 3.0,
                             "G": 4.0,
                             "Z": 5.0,
                             "K": 6.0,
                             "D": 7.0,
                             "V": 8.0,
                             "L": 9.0,
                             "M": 10.0,
                             "O": 11.0,
                             "N": 12.0,
                             "U": 13.0}

        self.dict_lexical_features_to_float = {"Sl": 1.0,
                                          "So": 2.0,
                                          "Pp": 3.0,
                                          "Pd": 4.0,
                                          "Ps": 5.0,
                                          "Rs": 6.0,
                                          "Rd": 7.0,
                                          "Gg": 8.0,
                                          "Gp": 9.0,
                                          "Zo": 10.0,
                                          "Zs": 11.0,
                                          "Zk": 12.0,
                                          "Zz": 13.0,
                                          "Zp": 14.0,
                                          "Zc": 15.0,
                                          "Zv": 16.0,
                                          "Zn": 17.0,
                                          "Zl": 18.0,
                                          "Ka": 19.0,
                                          "Kr": 20.0,
                                          "Kb": 21.0,
                                          "Di": 22.0,
                                          "Dr": 23.0,
                                          "Dd": 24.0,
                                          "Dt": 25.0,
                                          "Dm": 26.0,
                                          "Do": 27.0,
                                          "Vp": 28.0,
                                          "Vd": 29.0,
                                          "L": 30.0,
                                          "O": 31.0,
                                          "M": 32.0,
                                          "Nj": 33.0,
                                          "Nt": 34.0,
                                          "Nw": 35.0,
                                          "Ne": 36.0,
                                          "Nh": 37.0,
                                          "Na": 38.0,
                                          "Np": 39.0}

        self.dict_fpos_to_float = {"Slm": 0.0,
                                   "Slz": 1.0,
                                   "Sls": 2.0,
                                   "Som": 3.0,
                                   "Soz": 4.0,
                                   "Sos": 5.0,
                                   "Ps": 6.0,
                                   "Pp": 7.0,
                                   "Pd": 8.0,
                                   "Rs": 9.0,
                                   "Rd": 10.0,
                                   "Ggn": 11.0,
                                   "Ggd": 12.0,
                                   "Ggv": 13.0,
                                   "Gp-": 14.0,
                                   "Zo": 15.0,
                                   "Zs": 16.0,
                                   "Zk": 17.0,
                                   "Zz": 18.0,
                                   "Zp": 19.0,
                                   "Zc": 20.0,
                                   "Zv": 21.0,
                                   "Zn": 22.0,
                                   "Zl": 23.0,
                                   "Kag": 24.0,
                                   "Kav": 25.0,
                                   "Krg": 26.0,
                                   "Krv": 27.0,
                                   "Kbg": 28.0,
                                   "Kbv": 29.0,
                                   "Kbz": 30.0,
                                   "Kbd": 31.0,
                                   "Di": 32.0,
                                   "Dr": 33.0,
                                   "Dd": 34.0,
                                   "Dt": 35.0,
                                   "Dm": 36.0,
                                   "Do": 37.0,
                                   "Vp": 38.0,
                                   "Vd": 39.0,
                                   "L": 40.0,
                                   "O": 41.0,
                                   "M": 42.0,
                                   "Nj": 43.0,
                                   "Nt": 44.0,
                                   "Nw": 45.0,
                                   "Ne": 46.0,
                                   "Nh": 47.0,
                                   "Na": 48.0,
                                   "Np": 49.0
                                   }

        # COMPILE CVC CONVERSION DICTIONARIES
        self.CVC_ROBUST_conversion_dictionary = dd()
        self.CVC_FINEGRAINED_conversion_dictionary = dd()
        for line in open(os.path.join(resources_directory, "CVC_character_categorization.tsv"), "r", encoding="UTF-8").readlines()[1:]:  # SKIP HEADERS
            character_string, CV_ROBUST_category, CV_FINEGRAINED_category = line.strip("\n").split("\t")

            self.CVC_ROBUST_conversion_dictionary[character_string] = CV_ROBUST_category
            self.CVC_FINEGRAINED_conversion_dictionary[character_string] = CV_FINEGRAINED_category

        # LOAD LIST OF SLOVENE G2P CHARACTERS
        self.list_of_SLOVENE_G2P_CHARACTERS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "slovene_g2p_characters.tsv"), "r", encoding="UTF-8").readlines()[1:]]

        # LOAD LISTS OF CHARACTER NGRAMS
        self.list_of_GENERAL_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_GENERAL_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]
        self.list_of_ENDING_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_ENDING_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]
        self.list_of_STARTING_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_STARTING_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]

        # LOAD LISTS OF CVC NGRAMS (ROBUST)
        self.list_of_CVC_ROBUST_GENERAL_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_CVC_ROBUST_GENERAL_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]
        self.list_of_CVC_ROBUST_ENDING_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_CVC_ROBUST_ENDING_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]
        self.list_of_CVC_ROBUST_STARTING_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_CVC_ROBUST_STARTING_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]

        # LOAD LISTS OF CVC NGRAMS (FINEGRAINED)
        self.list_of_CVC_FINEGRAINED_GENERAL_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_CVC_FINEGRAINED_GENERAL_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]
        self.list_of_CVC_FINEGRAINED_ENDING_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_CVC_FINEGRAINED_ENDING_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]
        self.list_of_CVC_FINEGRAINED_STARTING_NGRAMS = [line.strip("\n").split("\t")[0] for line in open(os.path.join(resources_directory, "features_CVC_FINEGRAINED_STARTING_NGRAMS.tsv"), "r", encoding="UTF-8").readlines()[1:]]


    def get_percentage_of_slovene_characters_in_lemma(self, string):
        count_slovene_characters = 0
        for character in list(string):
            if character in self.list_of_SLOVENE_G2P_CHARACTERS:
                count_slovene_characters += 1

        return count_slovene_characters / len(list(string))


    def get_number_of_ngrams_within_lemma(self, string):
        # GET NUMBER OF UNIGRAMS
        nr_unigrams = len(list(string))
        # GET NUMBER OF BIGRAMS
        nr_bigrams = 0
        for index, character in enumerate(list(string)):
            try:
                character_1 = character
                character_2 = list(string)[index + 1]
                nr_bigrams += 1
            except:
                continue
        # GET NUMBER OF TRIGRAMS
        nr_trigrams = 0
        for index, character in enumerate(list(string)):
            try:
                character_1 = character
                character_2 = list(string)[index + 1]
                character_3 = list(string)[index + 2]
                nr_trigrams += 1
            except:
                continue

        return nr_unigrams, nr_bigrams, nr_trigrams


    def extract_starting_ngrams(self, string):
        dict_ngram_abs_frequency = dd(int)
        dict_ngram_rel_frequency = dd(float)
        nr_unigrams, nr_bigrams, nr_trigrams = self.get_number_of_ngrams_within_lemma(string=string)

        length_of_string = len(list(string))
        # STARTING UNIGRAM
        dict_ngram_abs_frequency[list(string)[0]] += 1
        # STARTING BIGRAM
        if length_of_string >= 2:
            dict_ngram_abs_frequency["".join(list(string)[0:2])] += 1
        # STARTING TRIGRAM
        if length_of_string >= 3:
            dict_ngram_abs_frequency["".join(list(string)[0:3])] += 1

        for x in dict_ngram_abs_frequency:
            if len(list(x)) == 1:
                dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / nr_unigrams
            elif len(list(x)) == 2:
                dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / nr_bigrams
            elif len(list(x)) == 3:
                dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / nr_trigrams

        return dict_ngram_abs_frequency, dict_ngram_rel_frequency


    def extract_ending_ngrams(self, string):
        dict_ngram_abs_frequency = dd(int)
        dict_ngram_rel_frequency = dd(float)
        nr_unigrams, nr_bigrams, nr_trigrams = self.get_number_of_ngrams_within_lemma(string=string)
        length_of_string = len(list(string))

        # ENDING UNIGRAM
        dict_ngram_abs_frequency[list(string)[-1]] += 1
        # STARTING BIGRAM
        if length_of_string >= 2:
            dict_ngram_abs_frequency["".join(list(string)[-2:])] += 1
        # STARTING TRIGRAM
        if length_of_string >= 3:
            dict_ngram_abs_frequency["".join(list(string)[-3:])] += 1

        for x in dict_ngram_abs_frequency:
            if len(list(x)) == 1:
                dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / nr_unigrams
            elif len(list(x)) == 2:
                dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / nr_bigrams
            elif len(list(x)) == 3:
                dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / nr_trigrams

        return dict_ngram_abs_frequency, dict_ngram_rel_frequency


    def extract_unigrams(self, string):
        dict_ngram_abs_frequency = dd(int)
        dict_ngram_rel_frequency = dd(float)
        total_number_of_ngrams_in_string = 0
        for character in list(string):
            dict_ngram_abs_frequency[character] += 1
            total_number_of_ngrams_in_string += 1

        for x in dict_ngram_abs_frequency:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / total_number_of_ngrams_in_string

        return dict_ngram_abs_frequency, dict_ngram_rel_frequency


    def extract_bigrams(self, string):
        dict_ngram_abs_frequency = dd(int)
        dict_ngram_rel_frequency = dd(float)
        total_number_of_ngrams_in_string = 0
        for index, character in enumerate(list(string)):
            try:
                character_1 = character
                character_2 = list(string)[index + 1]
                bigram = f"{character_1}{character_2}"
                dict_ngram_abs_frequency[bigram] += 1
                total_number_of_ngrams_in_string += 1
            except:
                continue

        for x in dict_ngram_abs_frequency:
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / total_number_of_ngrams_in_string

        return dict_ngram_abs_frequency, dict_ngram_rel_frequency


    def extract_trigrams(self, string):
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
            dict_ngram_rel_frequency[x] = dict_ngram_abs_frequency[x] / total_number_of_ngrams_in_string

        return dict_ngram_abs_frequency, dict_ngram_rel_frequency


    def get_features_based_on_morphosyntactic_tags(self, fpos):
        # GET FEATURES BASED ON MORPHOSYNTACTIC TAGS
        pos_feature = self.dict_pos_to_float[fpos[0]]
        lexical_feature = self.dict_lexical_features_to_float[fpos[0:2]]
        fpos_feature = self.dict_fpos_to_float[fpos]

        return pos_feature, lexical_feature, fpos_feature



    def get_ngram_features(self, lemma, list_of_unique_ngrams_for_vectorization, get_general_ngrams, get_starting_ngrams, get_ending_ngrams, ngram_type):
        frequency_dictionary_of_general_ngrams_in_lemma = dd(float)
        frequency_dictionary_of_ending_ngrams_in_lemma = dd(float)
        frequency_dictionary_of_starting_ngrams_in_lemma = dd(float)

        # NGRAM_TYPE - THIS IS INCLUDED IN THE NAME OF PLACEHOLDER NGRAMS TO DIFFERENTIATE BETWEEN placeholder_unigram (GENERAL), placeholder_unigram_CVC_ROBUST etc.
        if ngram_type == "general_character":
            additional_name = "GENERAL_CHARACTERS"
        elif ngram_type == "ending_character":
            additional_name = "ENDING_CHARACTERS"
        elif ngram_type == "starting_character":
            additional_name = "STARTING_CHARACTERS"
        elif ngram_type == "general_cvc_robust":
            additional_name = "GENERAL_CVC_ROBUST"
        elif ngram_type == "ending_cvc_robust":
            additional_name = "ENDING_CVC_ROBUST"
        elif ngram_type == "starting_cvc_robust":
            additional_name = "STARTING_CVC_ROBUST"
        elif ngram_type == "general_cvc_finegrained":
            additional_name = "GENERAL_CVC_FINEGRAINED"
        elif ngram_type == "ending_cvc_finegrained":
            additional_name = "ENDING_CVC_FINEGRAINED"
        elif ngram_type == "starting_cvc_finegrained":
            additional_name = "STARTING_CVC_FINEGRAINED"

        # POPULATE DICTIONARIES WITH ALL UNIQUE NGRAMS
        for unique_ngram in list_of_unique_ngrams_for_vectorization:
            frequency_dictionary_of_general_ngrams_in_lemma[unique_ngram] = 0.0
            frequency_dictionary_of_ending_ngrams_in_lemma[unique_ngram] = 0.0
            frequency_dictionary_of_starting_ngrams_in_lemma[unique_ngram] = 0.0
        # + A PLACEHOLDER NGRAM FOR ALL OTHER POTENTIAL NGRAMS NOT SEEN IN THIS INITIAL BATCH
        frequency_dictionary_of_general_ngrams_in_lemma[f'placeholder_unigram_{additional_name}'] = 0.0
        frequency_dictionary_of_starting_ngrams_in_lemma[f'placeholder_unigram_{additional_name}'] = 0.0
        frequency_dictionary_of_ending_ngrams_in_lemma[f'placeholder_unigram_{additional_name}'] = 0.0
        frequency_dictionary_of_general_ngrams_in_lemma[f'placeholder_bigram_{additional_name}'] = 0.0
        frequency_dictionary_of_starting_ngrams_in_lemma[f'placeholder_bigram_{additional_name}'] = 0.0
        frequency_dictionary_of_ending_ngrams_in_lemma[f'placeholder_bigram_{additional_name}'] = 0.0
        frequency_dictionary_of_general_ngrams_in_lemma[f'placeholder_trigram_{additional_name}'] = 0.0
        frequency_dictionary_of_starting_ngrams_in_lemma[f'placeholder_trigram_{additional_name}'] = 0.0
        frequency_dictionary_of_ending_ngrams_in_lemma[f'placeholder_trigram_{additional_name}'] = 0.0


        if get_general_ngrams:
            # EXTRACT UNIGRAMS FROM LEMMA
            unigrams_dict_abs, unigrams_dict_rel = self.extract_unigrams(string=lemma)

            for unigram in unigrams_dict_rel:
                if unigram in frequency_dictionary_of_general_ngrams_in_lemma:
                    frequency_dictionary_of_general_ngrams_in_lemma[unigram] += unigrams_dict_rel[unigram]
                else:
                    frequency_dictionary_of_general_ngrams_in_lemma[f'placeholder_unigram_{additional_name}'] += unigrams_dict_rel[unigram]

            # EXTRACT BIGRAMS FROM LEMMA
            bigrams_dict_abs, bigrams_dict_rel = self.extract_bigrams(string=lemma)

            for bigram in bigrams_dict_rel:
                if bigram in frequency_dictionary_of_general_ngrams_in_lemma:
                    frequency_dictionary_of_general_ngrams_in_lemma[bigram] += bigrams_dict_rel[bigram]
                else:
                    frequency_dictionary_of_general_ngrams_in_lemma[f'placeholder_bigram_{additional_name}'] += bigrams_dict_rel[bigram]

            # EXTRACT TRIGRAMS FROM LEMMA
            trigrams_dict_abs, trigrams_dict_rel = self.extract_trigrams(string=lemma)

            for trigram in trigrams_dict_rel:
                if trigram in frequency_dictionary_of_general_ngrams_in_lemma:
                    frequency_dictionary_of_general_ngrams_in_lemma[trigram] += trigrams_dict_rel[trigram]
                else:
                    frequency_dictionary_of_general_ngrams_in_lemma[f'placeholder_trigram_{additional_name}'] += trigrams_dict_rel[trigram]

        if get_ending_ngrams:
            # EXTRACT ENDING NGRAMS FROM LEMMA
            ending_ngrams_abs, ending_ngrams_rel = self.extract_ending_ngrams(string=lemma)

            for ending_ngram in ending_ngrams_rel:
                if ending_ngram in frequency_dictionary_of_ending_ngrams_in_lemma:
                    frequency_dictionary_of_ending_ngrams_in_lemma[ending_ngram] += ending_ngrams_rel[ending_ngram]
                else:
                    if len(list(ending_ngram)) == 1:
                        frequency_dictionary_of_ending_ngrams_in_lemma[f'placeholder_unigram_{additional_name}'] += ending_ngrams_rel[ending_ngram]
                    elif len(list(ending_ngram)) == 2:
                        frequency_dictionary_of_ending_ngrams_in_lemma[f'placeholder_bigram_{additional_name}'] += ending_ngrams_rel[ending_ngram]
                    elif len(list(ending_ngram)) == 3:
                        frequency_dictionary_of_ending_ngrams_in_lemma[f'placeholder_trigram_{additional_name}'] += ending_ngrams_rel[ending_ngram]

        if get_starting_ngrams:
            # EXTRACT STARTING NGRAMS FROM LEMMA
            starting_ngrams_abs, starting_ngrams_rel = self.extract_starting_ngrams(string=lemma)

            for starting_ngram in starting_ngrams_rel:
                if starting_ngram in frequency_dictionary_of_starting_ngrams_in_lemma:
                    frequency_dictionary_of_starting_ngrams_in_lemma[starting_ngram] = starting_ngrams_rel[starting_ngram]
                else:
                    if len(list(starting_ngram)) == 1:
                        frequency_dictionary_of_starting_ngrams_in_lemma[f'placeholder_unigram_{additional_name}'] = starting_ngrams_rel[starting_ngram]
                    elif len(list(starting_ngram)) == 2:
                        frequency_dictionary_of_starting_ngrams_in_lemma[f'placeholder_bigram_{additional_name}'] = starting_ngrams_rel[starting_ngram]
                    elif len(list(starting_ngram)) == 3:
                        frequency_dictionary_of_starting_ngrams_in_lemma[f'placeholder_trigram_{additional_name}'] = starting_ngrams_rel[starting_ngram]

        list_of_feature_names = []
        #list_of_feature_names.append("pos")
        #list_of_feature_names.append("lexical_feature")
        #list_of_feature_names.append("fpos")
        #list_of_feature_names.append("percent_slovene_characters")

        if get_general_ngrams:
            # ADD NGRAMS IN GENERAL
            for ngram in frequency_dictionary_of_general_ngrams_in_lemma:
                list_of_feature_names.append(ngram)

        if get_ending_ngrams:
            # ADD NAMES OF ENDING NGRAMS
            for ngram in frequency_dictionary_of_ending_ngrams_in_lemma:
                if not "|END|" in ngram:
                    list_of_feature_names.append(f"{ngram}|END|")
                else:
                    list_of_feature_names.append(f"{ngram}")

        if get_starting_ngrams:
            # ADD NAMES OF STARTING NGRAMS
            for ngram in frequency_dictionary_of_starting_ngrams_in_lemma:
                if not "|BEG|" in ngram:
                    list_of_feature_names.append(f"|BEG|{ngram}")
                else:
                    list_of_feature_names.append(f"{ngram}")

        list_of_features = []
        #list_of_features.append(pos_feature)
        #list_of_features.append(lexical_feature)
        #list_of_features.append(fpos_feature)
        #list_of_features.append(percentage_of_slovene_characters)

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


    def convert_to_CVC(self, string, conversion_dictionary):
        converted_characters = []
        for character in list(string):
            if character in conversion_dictionary:
                converted_characters.append(conversion_dictionary[character])
            else:
                converted_characters.append("-")

        return "".join(converted_characters)


    def vectorize_lemfpos(self, lemma, fpos):

        list_of_all_features = []
        list_of_all_feature_names = []

        # CONVERT LEMMA TO LOWERCASE
        lc_lemma = lemma.lower()

        # GET FEATURES BASED ON MORPHOSYNTACTIC TAGS
        pos_feature, lexical_feature, fpos_feature = self.get_features_based_on_morphosyntactic_tags(fpos=fpos)
        for feature, feature_name in [(pos_feature, "pos_feature"), (lexical_feature, "lexical_feature"), (fpos_feature, "fpos_feature")]:
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURE BASED ON SLOVENE G2P CHARACTERS
        percent_slovene_characters = self.get_percentage_of_slovene_characters_in_lemma(string=lc_lemma)
        list_of_all_features.append(percent_slovene_characters)
        list_of_all_feature_names.append("percent_slovene_characters")

        # GET FEATURES - GENERAL CHARACTER NGRAMS
        features_GENERAL_CHARACTER_NGRAMS, feature_names_GENERAL_CHARACTER_NGRAMS = self.get_ngram_features(lemma=lc_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_GENERAL_NGRAMS, get_ending_ngrams=False, get_starting_ngrams=False, get_general_ngrams=True, ngram_type='general_character')
        for feature, feature_name in zip(features_GENERAL_CHARACTER_NGRAMS, feature_names_GENERAL_CHARACTER_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURES - ENDING CHARACTER NGRAMS
        features_ENDING_CHARACTER_NGRAMS, feature_names_ENDING_CHARACTER_NGRAMS = self.get_ngram_features(lemma=lc_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_ENDING_NGRAMS, get_ending_ngrams=True, get_starting_ngrams=False, get_general_ngrams=False, ngram_type='ending_character')
        for feature, feature_name in zip(features_ENDING_CHARACTER_NGRAMS, feature_names_ENDING_CHARACTER_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURES - STARTING CHARACTER NGRAMS
        features_STARTING_CHARACTER_NGRAMS, feature_names_STARTING_CHARACTER_NGRAMS = self.get_ngram_features(lemma=lc_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_STARTING_NGRAMS, get_ending_ngrams=False, get_starting_ngrams=True, get_general_ngrams=False, ngram_type='starting_character')
        for feature, feature_name in zip(features_STARTING_CHARACTER_NGRAMS, feature_names_STARTING_CHARACTER_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # CONVERT LEMMA TO CVC (ROBUST)
        CVC_ROBUST_lemma = self.convert_to_CVC(string=lc_lemma, conversion_dictionary=self.CVC_ROBUST_conversion_dictionary)

        # GET FEATURES - GENERAL CVC-ROBUST NGRAMS
        features_GENERAL_CVC_ROBUST_NGRAMS, feature_names_GENERAL_CVC_ROBUST_NGRAMS = self.get_ngram_features(lemma=CVC_ROBUST_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_CVC_ROBUST_GENERAL_NGRAMS, get_ending_ngrams=False, get_starting_ngrams=False, get_general_ngrams=True, ngram_type='general_cvc_robust')
        for feature, feature_name in zip(features_GENERAL_CVC_ROBUST_NGRAMS, feature_names_GENERAL_CVC_ROBUST_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURES - ENDING CVC-ROBUST NGRAMS
        features_ENDING_CVC_ROBUST_NGRAMS, feature_names_ENDING_CVC_ROBUST_NGRAMS = self.get_ngram_features(lemma=CVC_ROBUST_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_CVC_ROBUST_ENDING_NGRAMS, get_ending_ngrams=True, get_starting_ngrams=False, get_general_ngrams=False, ngram_type='ending_cvc_robust')
        for feature, feature_name in zip(features_ENDING_CVC_ROBUST_NGRAMS, feature_names_ENDING_CVC_ROBUST_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURES - STARTING CVC-ROBUST NGRAMS
        features_STARTING_CVC_ROBUST_NGRAMS, feature_names_STARTING_CVC_ROBUST_NGRAMS = self.get_ngram_features(lemma=CVC_ROBUST_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_CVC_ROBUST_STARTING_NGRAMS, get_ending_ngrams=False, get_starting_ngrams=True, get_general_ngrams=False, ngram_type='starting_cvc_robust')
        for feature, feature_name in zip(features_STARTING_CVC_ROBUST_NGRAMS, feature_names_STARTING_CVC_ROBUST_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # CONVERT LEMMA TO CVC (FINEGRAINED)
        CVC_FINEGRAINED_lemma = self.convert_to_CVC(string=lc_lemma, conversion_dictionary=self.CVC_FINEGRAINED_conversion_dictionary)

        # GET FEATURES - GENERAL CVC-FINEGRAINED NGRAMS
        features_GENERAL_CVC_FINEGRAINED_NGRAMS, feature_names_GENERAL_CVC_FINEGRAINED_NGRAMS = self.get_ngram_features(lemma=CVC_FINEGRAINED_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_CVC_FINEGRAINED_GENERAL_NGRAMS, get_ending_ngrams=False, get_starting_ngrams=False, get_general_ngrams=True, ngram_type='general_cvc_finegrained')
        for feature, feature_name in zip(features_GENERAL_CVC_FINEGRAINED_NGRAMS, feature_names_GENERAL_CVC_FINEGRAINED_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURES - ENDING CVC-FINEGRAINED NGRAMS
        features_ENDING_CVC_FINEGRAINED_NGRAMS, feature_names_ENDING_CVC_FINEGRAINED_NGRAMS = self.get_ngram_features(lemma=CVC_FINEGRAINED_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_CVC_FINEGRAINED_ENDING_NGRAMS, get_ending_ngrams=True, get_starting_ngrams=False, get_general_ngrams=False, ngram_type='ending_cvc_finegrained')
        for feature, feature_name in zip(features_ENDING_CVC_FINEGRAINED_NGRAMS, feature_names_ENDING_CVC_FINEGRAINED_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        # GET FEATURES - STARTING CVC-FINEGRAINED NGRAMS
        features_STARTING_CVC_FINEGRAINED_NGRAMS, feature_names_STARTING_CVC_FINEGRAINED_NGRAMS = self.get_ngram_features(lemma=CVC_FINEGRAINED_lemma, list_of_unique_ngrams_for_vectorization=self.list_of_CVC_FINEGRAINED_STARTING_NGRAMS, get_ending_ngrams=False, get_starting_ngrams=True, get_general_ngrams=False, ngram_type='starting_cvc_finegrained')
        for feature, feature_name in zip(features_STARTING_CVC_FINEGRAINED_NGRAMS, feature_names_STARTING_CVC_FINEGRAINED_NGRAMS):
            list_of_all_features.append(feature)
            list_of_all_feature_names.append(feature_name)

        return list_of_all_features, list_of_all_feature_names


# INSTANTIATE VECTORIZER
vectorizer = Vectorizer(resources_directory="./ngram_lists/")

# GET FILE WITH G2P ANNOTATIONS FROM SLOLEKS AND GET LIST OF TRAINING DATA
file_with_lemmas = open("lemfpos_and_pronunciation_type_MANUAL_CORRECTIONS.tsv", "r", encoding="UTF-8").readlines()
list_of_g2p_annotations = []
list_of_feature_vectors = []
list_of_lemfpos_and_sloleks_ids = []

count_processed_lines = 0
for line in file_with_lemmas[1:]:  # SKIP HEADERS
    sloleks_id,\
    lemma,\
    fpos,\
    pronunciation_type,\
    entry_status = line.strip("\n").split("\t")

    count_processed_lines += 1
    if count_processed_lines % 10000 == 0:
        print(f"{count_processed_lines} lines processed.")

    if pronunciation_type in ["Slovene G2P", "Slovene G2P with minor deviation"]:
        pronunciation_type = "Slovene G2P"
    elif pronunciation_type in ["Other G2P"]:
        pronunciation_type = "Other G2P"

    if pronunciation_type in ["Slovene G2P", "Other G2P"]:
        features, names = vectorizer.vectorize_lemfpos(lemma=lemma, fpos=fpos)
        list_of_feature_vectors.append(features)
        list_of_g2p_annotations.append(pronunciation_type)
        list_of_lemfpos_and_sloleks_ids.append(f"{lemma}{sep}{fpos}{sep}{sloleks_id}")


# https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
# LINEAR SUPPORT VECTOR CLASSIFICATION
classifier = LinearSVC()
model = classifier.fit(list_of_feature_vectors, list_of_g2p_annotations)


# SAVE MODELS
pickle.dump(model, open('final_LinearSVC_model_export.sav', 'wb'))

