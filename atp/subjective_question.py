""" 
@Author: kumar.nityan.suman
@Date: 2018-03-07 17:00:49
@Last Modified time: 2019-01-19 16:31:49
"""


import nltk as nlp
from nltk.corpus import stopwords
import numpy as np


# question patterns
question_formats = [
    "Explain in detail ",
    "Define ",
    "Write a short note on ",
    "What do you mean by "
    ]


# grammer to chunk keywords
grammer = r"""
    CHUNK: {<NN>+<IN|DT>*<NN>+}
    {<NN>+<IN|DT>*<NNP>+}
    {<NNP>+<NNS>*}
    """


def generate_subj_question(filepath):
    # open file and load data
    fp = open(filepath, mode="r")
    data = fp.read()
    fp.close()
    # get sentences from the data
    sentences = nlp.sent_tokenize(data)
    # get english stopwords
    stop_words = list(stopwords.words("english"))
    que_ans_dict = dict()
    # train the regex parser on the above grammer
    cp = nlp.RegexpParser(grammer)
    # select imp sentence to generate questions
    for sentence in sentences:
        # make words out of the sentence
        tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
        # parse the words to select the imp keywords to generate questions
        tree = cp.parse(tagged_words)
        for subtree in tree.subtrees():
            if subtree.label() == "CHUNK":
                # temp data handler
                temp = ""
                # traverse through the subtree
                for sub in subtree:
                    temp += sub[0]
                    temp += " "
                temp = temp.strip()
                temp = temp.upper()
                # select keyword and answer
                if temp not in que_ans_dict:
                    if len(nlp.word_tokenize(sentence)) > 20:
                        que_ans_dict[temp] = sentence
                else:
                    que_ans_dict[temp] += sentence
    # get a list of all keywords
    keyword_list = list(que_ans_dict.keys())
    que_ans_pair2 = list()
    # form questions
    for x in range(3):
        rand_num = np.random.randint(0, len(keyword_list))
        selected_key = keyword_list[rand_num]
        answer = que_ans_dict[selected_key]
        # get a question format
        rand_num %= 4
        que_format = question_formats[rand_num]
        # form question
        question = que_format + selected_key + "."
        # make a dictionary and append to the main list repo
        que_ans_pair2.append({"Question": question, "Answer": answer})
    return que_ans_pair2