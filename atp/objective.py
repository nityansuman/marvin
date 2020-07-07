# Copyright 2020 The `Kumar Nityan Suman` (https://github.com/nityansuman/). All Rights Reserved.
#
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
# ==============================================================================


# Import packages
import os
import re
import sys
import nltk
import numpy as np
from nltk.corpus import wordnet as wn
from textblob import TextBlob


class ObjectiveTest:
    """Class abstraction for objective test generation module
    """

    def __init__(self, filepath):
        """Class constructor
        
        Arguments:
            filepath {str} -- Absolute path to the corpus file
        """
        try:
            with open(filepath, mode="r") as fp:
                self.summary = fp.read()
        except FileNotFoundError as e:
            print("Warning raised at `ObjectiveTest.__init__`", e)

    def get_trivial_sentences(self):
        """Method to dentify sentences with potential to create objective questions
        
        Returns:
            list -- Sentences with potential to create objective questions
        """
        # Sentence tokenization
        sentences = nltk.sent_tokenize(self.summary)
        trivial_sentences = list()
        # Identify trivial sentences
        for sent in sentences:
            trivial = self.identify_trivial_sentences(sent)
            if trivial:
                trivial_sentences.append(trivial)
            else:
                continue
        return trivial_sentences

    def identify_trivial_sentences(self, sentence):
        """Method to evaluate if a given sentence has the potential to generate an objective question.
        
        Arguments:
            sentence {str} -- String sequence generated from a `sentence_tokenizer`
        
        Returns:
            dict -- Question formed along with the correct answer in case of potential sentence
                    else return `None`
        """
        # If sentence starts with an adverb or is less than 4 words long probably not the best fit
        tags = nltk.pos_tag(sentence)
        if tags[0][1] == "RB" or len(nltk.word_tokenize(sentence)) < 4:
            return None
        
        # Extract noun phrases from the sentence
        noun_phrases = list()
        grammer = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                {<NN>+<IN|DT>*<NNP>+}
                {<NNP>+<NNS>*}
            """
        chunker = nltk.RegexpParser(grammer)
        tokens = nltk.word_tokenize(sentence)
        pos_tokens = nltk.tag.pos_tag(tokens)
        tree = chunker.parse(pos_tokens)

        # Select phrase
        for subtree in tree.subtrees():
            if subtree.label() == "CHUNK":
                temp = ""
                for sub in subtree:
                    temp += sub[0]
                    temp += " "
                temp = temp.strip()
                noun_phrases.append(temp)
        
        # Replace nouns
        replace_nouns = []
        for word, _ in tags:
            for phrase in noun_phrases:
                if phrase[0] == '\'':
                    # If it starts with an apostrophe, ignore it
                    # (this is a weird error that should probably be handled elsewhere)
                    break
                if word in phrase:
                    # Blank out the last two words in this phrase
                    [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
                    break
            # If we couldn't find the word in any phrases
            if len(replace_nouns) == 0:
                replace_nouns.append(word)
            break
        
        if len(replace_nouns) == 0:
            # Return none if we found no words to replace
            return None
        
        val = 99
        for i in replace_nouns:
            if len(i) < val:
                val = len(i)
            else:
                continue
        
        trivial = {
            "Answer": " ".join(replace_nouns),
            "Key": val
        }

        if len(replace_nouns) == 1:
            # If we're only replacing one word, use WordNet to find similar words
            trivial["Similar"] = self.answer_options(replace_nouns[0])
        else:
            # If we're replacing a phrase, don't bother - it's too unlikely to make sense
            trivial["Similar"] = []
        
        # Blank out our replace words (only the first occurrence of the word in the sentence)
        replace_phrase = " ".join(replace_nouns)
        blanks_phrase = ("__________" * len(replace_nouns)).strip()
        # Compile regular expresession
        expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
        sentence = expression.sub(blanks_phrase, str(sentence), count=1)
        trivial["Question"] = sentence
        return trivial

    @staticmethod
    def answer_options(word):
        """Method to identify objective answer options
        
        Arguments:
            word {str} -- Actual answer to the question which is to be used for generating other deceiving options
        
        Returns:
            list -- Other answer options
        """
        # In the absence of a better method, take the first synset
        synsets = wn.synsets(word, pos="n")

        # If there aren't any synsets, return an empty list
        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]
        
        # Get the hypernym for this synset (again, take the first)
        hypernym = synset.hypernyms()[0]
        # Get some hyponyms from this hypernym
        hyponyms = hypernym.hyponyms()
        # Take the name of the first lemma for the first 8 hyponyms
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace("_", " ")
            if similar_word != word:
                similar_words.append(similar_word)
            if len(similar_words) == 8:
                break
        return similar_words

    def generate_test(self, num_of_questions=3):
        """Method to generate an objective test i.e., a set of questions and required options for answer.

        Arguments:
            num_of_questions {int} -- Integer denoting number of questions to set in the test.
        
        Returns:
            list, list -- A pair of lists containing questions and answer options respectively.
        """
        trivial_pair = self.get_trivial_sentences()
        question_answer = list()
        for que_ans_dict in trivial_pair:
            if que_ans_dict["Key"] > 3:
                question_answer.append(que_ans_dict)
            else:
                continue
        question = list()
        answer = list()
        while len(question) < num_of_questions:
            rand_num = np.random.randint(0, len(question_answer))
            if question_answer[rand_num]["Question"] not in question:
                question.append(question_answer[rand_num]["Question"])
                answer.append(question_answer[rand_num]["Answer"])
            else:
                continue
        return question, answer