""" 
@Author: Kumar Nityan Suman
@Date: 2018-05-01 21:00:01
@Last Modified time: 2019-01-19 16:32:34
"""


import os
import csv
import numpy as np
import pandas as pd
from datetime import datetime
from atp.article import Article


subjective_path = str(os.getcwd()) + "/atp/static/data/db/user_data_log_subjective.csv"
objective_path = str(os.getcwd()) +  "/atp/static/data/db/user_data_log_objective.csv"


def back_up_data(uname, subject_name, score_obt, flag):
    # open the database file and save the score
    user_name_list = uname.split()
    uname = "_".join(user_name_list)
    uname = uname.upper()

    subject_name = subject_name.strip().upper()
    if flag == "1":
        filepath = objective_path
    else:
        filepath = subjective_path
    date = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year

    row = [date, month, year, uname, subject_name, score_obt]
    
    # create a new file and write to it
    with open(filepath, mode="a") as fp:
        fp_writer = csv.writer(fp)
        fp_writer.writerow(row)
    return True


def get_obj_question(pair):
    que = list()
    ans = list()
    while len(que) < 3:
        # generate a random number
        rand_num = np.random.randint(0, len(pair))
        # get the que and ans to theat corresponding number
        new_list_dict = pair[rand_num]
        if new_list_dict["Question"] not in que:
            que.append(new_list_dict["Question"])
            ans.append(new_list_dict["Answer"])
        else:
            continue
    return que, ans


def get_sbj_question(pair):
    que = list()
    ans = list()
    while len(que) < 2:
        # generate a random number
        rand_num = np.random.randint(0, len(pair))
        # get the que and ans to theat corresponding number
        new_list_dict = pair[rand_num]
        if new_list_dict["Question"] not in que:
            que.append(new_list_dict["Question"])
            ans.append(new_list_dict["Answer"])
        else:
            continue
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
            if que["Anser_key"] > 3:
                que_ans_pair.append(que)
            else:
                continue
    return que_ans_pair


def relative_ranking(subjectname, flag):
    # load the data from file
    subjectname = subjectname.upper()
    
    if flag == "1":
        df = pd.read_csv(objective_path)
    else:
        df = pd.read_csv(subjective_path)
    
    # get the datframe with a particular subject
    temp_df = df[df["SUBJECT_NAME"] == subjectname]
    
    # find the maximum and minimum marks scored in that subject
    max_score = max(temp_df["SCORE"])
    min_score = min(temp_df["SCORE"])
    mean_score = temp_df["SCORE"].mean()
    return max_score, mean_score, min_score
