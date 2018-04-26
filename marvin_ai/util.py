from marvin_ai.article import Article
import numpy as np
import pandas as pd
import os
import csv
from datetime import datetime


def back_up_data(uname, subject_name, score_obt, flag):
    # open the database file and save the score
    user_name_list = uname.split(" ")
    uname = "_".join(user_name_list)
    uname = uname.upper()

    subject_name = subject_name.strip(" ").upper()
    if flag == "1":
        filepath = "/mnt/d/automating-the-examination-system/marvin_ai/static/data/db/user-data-log.csv"
    else:
        filepath = "/mnt/d/automating-the-examination-system/marvin_ai/static/data/db/user-data-log_2.csv"
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
        df = pd.read_csv("/mnt/d/automating-the-examination-system/marvin_ai/static/data/db/user-data-log.csv", header=0)
    else:
        df = pd.read_csv("/mnt/d/automating-the-examination-system/marvin_ai/static/data/db/user-data-log_2.csv", header=0)
    
    # get the datframe with a particular subject
    temp_df = df[df["SUBJECT_NAME"] == subjectname]
    
    # find the maximum and minimum marks scored in that subject
    max_score = max(temp_df["SCORE"])
    min_score = min(temp_df["SCORE"])
    mean_score = temp_df["SCORE"].mean()
    return max_score, mean_score, min_score