import matplotlib.pyplot as plt
from marvin_ai.article import Article
import numpy as np
import pandas as pd
import os
import csv
from datetime import datetime


def back_up_data(uname, subject_name, score_obt):
    # open the database file and save the score
    user_name_list = uname.split(" ")
    uname = "_".join(user_name_list)
    filepath = "/mnt/d/automating-the-examination-system/marvin_ai/static/data/db/user-data-log.csv"
    date = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year

    row = [date, month, year, uname, subject_name, score_obt]
    
    if os.path.isfile(filepath) == True:
        # file exists then append row
        fp = open(filepath, mode="a")
        fp_writer = csv.writer(fp)
        fp_writer.writerow(row)
        
        fp.close()
    else:
        # create a new file and write to it
        fp = open(filepath, mode="w")
        fp_writer = csv.writer(fp)
        fp_writer.writerow(["DATE", "MONTH", "YEAR", "USERNAME", "SUBJECT_NAME", "SCORE"])
        fp_writer.writerow(row)

        fp.close()
    # return status
    return True


def get_a_question(pair):
    # generate a random number
    rand_num = np.random.randint(0, len(pair))
    # get the que and ans to theat corresponding number
    que = pair[rand_num]["Question"]
    ans = pair[rand_num]["Answer"]
    return que, ans


def generate_trivia(filename):
    # Retrieve the trivia sentences
    questions = list()
    # create an object
    obj_a = Article(filename)
    # call method on the object
    questions.append(obj_a.generate_trivia_sentences())
    # list to store que and ans in the form of a dictionary
    que_ans_pair = list()
    for lis in questions:
        for que in lis:
            if que["Anser_key"] > 4:
                que_ans_pair.append(que)
            else:
                continue
    return que_ans_pair
