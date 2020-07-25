# Copyright 2020 The `Kumar Nityan Suman` (https://github.com/nityansuman/). All Rights Reserved.
#
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
# ==============================================================================


# Import packages
import numpy as np
import nltk as nlp


class SubjectiveTest:
    """Class abstraction for subjective test generation module.
    """

    def __init__(self, filepath):
        """Class constructor.
        
        Arguments:
            filepath {str} -- String representing the filepath for the subject corpus.
        """
        # Question pattern
        self.question_pattern = [
            "Explain in detail ",
            "Define ",
            "Write a short note on ",
            "What do you mean by "
        ]
        # Grammar to chunk keywords
        self.grammar = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
            {<NN>+<IN|DT>*<NNP>+}
            {<NNP>+<NNS>*}
        """
        self.filepath = filepath
        try:
            with open(filepath, mode="r") as fp:
                self.summary = fp.read()
        except FileNotFoundError as e:
            print(e)
    
    @staticmethod
    def word_tokenizer(sequence):
        """Tokenize string sequence on word level
        
        Arguments:
            sequence {str} -- String sequence
        
        Returns:
            list -- Contains word tokens out of the string sequence
        """
        # Perform sentence tokenization and word tokenization in a nested fashion
        word_tokens = list()
        for sent in nlp.sent_tokenize(sequence):
            for w in nlp.word_tokenize(sent):
                word_tokens.append(w)
        return word_tokens
    
    @staticmethod
    def create_vector(answer_tokens, tokens):
        """Create a one-hot encoded vector for the  answer_tokens` on the basis of `tokens`
        
        Arguments:
            answer_tokens {list} -- Tokenized user answer
            tokens {list} -- Tokenized actual answer corpus
        
        Returns:
            numpy.array -- A one-hot encoded vector of the answer
        """
        return np.array([1 if tok in answer_tokens else 0 for tok in tokens])
    
    @staticmethod
    def cosine_similarity_score(vector1, vector2):
        """Cmpute the euqlidean distance between teo vectors
        
        Arguments:
            vector1 {numpy.array} -- Actual answer vector
            vector2 {numpy.array} -- User answer vector
        
        Returns:
            float -- Distance between two vectors
        """
        def vector_value(vector):
            """Compute the value of a given vector
            
            Arguments:
                vector {numpy.array} -- Vector array
            
            Returns:
                float -- Value of the n-dimensional vector
            """
            return np.sqrt(np.sum(np.square(vector)))
        # Get vector value
        v1 = vector_value(vector1)
        v2 = vector_value(vector2)
        # Compute euclidean distance
        v1_v2 = np.dot(vector1, vector2)
        return (v1_v2 / (v1 * v2)) * 100
    
    def generate_test(self, num_of_questions=2):
        """Method to generate subjective test

        Arguments:
            num_of_questions {int} -- Maximum number of questions to generated
        
        Returns:
            list, list -- Generated `Questions` and `Answers` respectively
        """
        sentences = nlp.sent_tokenize(self.summary)
        # Train the regex parser on the above grammer
        cp = nlp.RegexpParser(self.grammar)
        question_answer_dict = dict()
        # Select imp sentence to generate questions
        for sentence in sentences:
            tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
            # Parse the words to select the imp keywords to generate questions
            tree = cp.parse(tagged_words)
            for subtree in tree.subtrees():
                if subtree.label() == "CHUNK":
                    temp = ""
                    # Traverse through the subtree
                    for sub in subtree:
                        temp += sub[0]
                        temp += " "
                    temp = temp.strip()
                    temp = temp.upper()
                    if temp not in question_answer_dict:
                        if len(nlp.word_tokenize(sentence)) > 20:
                            question_answer_dict[temp] = sentence
                    else:
                        question_answer_dict[temp] += sentence
        # Get a list of all keywords
        keyword_list = list(question_answer_dict.keys())
        question_answer = list()
        # Identify questions and their respective answers
        for _ in range(3):
            rand_num = np.random.randint(0, len(keyword_list))
            selected_key = keyword_list[rand_num]
            answer = question_answer_dict[selected_key]
            rand_num %= 4
            question = self.question_pattern[rand_num] + selected_key + "."
            # Make a dictionary and append to the main list repo
            question_answer.append({"Question": question, "Answer": answer})
        # Build separate containers
        que = list()
        ans = list()
        while len(que) < num_of_questions:
            rand_num = np.random.randint(0, len(question_answer))
            if question_answer[rand_num]["Question"] not in que:
                que.append(question_answer[rand_num]["Question"])
                ans.append(question_answer[rand_num]["Answer"])
            else:
                continue
        return que, ans
    
    def evaluate_subjective_answer(self, original_answer, user_answer):
        """Evaluate the subjective answer given by the user.
        
        Arguments:
            original_answer {str} -- A string representing the original asnwer.
            user_answer {str} -- A string representing the answer given by the user.
        
        Returns:
            float -- A floating point value indicating the similarity/correctness score of the user answer based on the original asnwer.
        """
        score_obt = 0
        original_ans_list = self.word_tokenizer(original_answer)
        user_ans_list = self.word_tokenizer(user_answer)
        # Join both word based vectors to get the overall vector
        overall_list = original_ans_list + user_ans_list
        # Create numeric vectors for both original answer and user answer based on the overall vector
        vector1 = self.create_vector(original_ans_list, overall_list)
        vector2 = self.create_vector(user_answer, overall_list)
        # Compute the similary score between the original ans vector and user ans vector
        score_obt = self.cosine_similarity_score(vector1, vector2)
        return score_obt