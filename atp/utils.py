# Copyright 2020 The `Kumar Nityan Suman` (https://github.com/nityansuman/). All Rights Reserved.
#
#
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
# ==============================================================================


# Import packages
import os
import os
import csv
import nltk as nlp
import numpy as np
import pandas as pd
from datetime import datetime


def back_up_data(username, subject_name, date, type, score, path):
    """Method to backup user test information
    
    Arguments:
        username {str} -- Name of the user
        subject_name {str} -- Name of the subject
        date {datetime} -- Date of the test taken
        type {str} -- Type of the test taken ("0": Objective, "1": Subjective)
        score {int} -- Total marks obtained by the user
    
    Returns:
        bool -- type indicating data backup status
    """
    # Transform username and subject_name for backup
    username = "_".join([x.upper() for x in username.split()])
    subject_name = subject_name.strip().upper()
    # Access calendar features
    date = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    # Create a row for backup
    column_names = ["Date", "Month", "Year", "Username", "Subject", "Score"]
    row = [date, month, year, username, subject_name, score] # Format of the CSV file
    # Check for a valid filepath
    file_exists = os.path.isfile(path)
    if file_exists:
        # If file exists, open file in append mode
        try:
            with open(path, mode="a") as fp:
                fp_writer = csv.writer(fp)
                # Backup data
                fp_writer.writerow(row)
                return True
        except Exception as e:
            print(e)
    else:
        # If file doesn't exists, create a new backup file
        try:
            with open(path, mode="w") as fp:
                fp_writer = csv.writer(fp)
                # Write header
                fp_writer.writerow(column_names)
                # Backup data
                fp_writer.writerow(row)
                return True
        except Exception as e:
            print(e)
    return False


def relative_ranking(subjectname, type, path):
    """Method to compute relative ranking of user on a particular subject.
    
    Arguments:
        subjectname {str} -- Name of the test subject.
        type {str} -- Denoting the type of the test taken
    
    Returns:
        int, float, int -- Maximum, Minimum and Average score obtained by the user in a paarticular subject test
    """
    subjectname = subjectname.upper()
    df = pd.read_csv(path)
    df = df[(df["SUBJECT"] == subjectname) & (df["TYPE"] == type)].copy()
    max_score = max(df["SCORE"])
    min_score = min(df["SCORE"])
    mean_score = df["SCORE"].mean()
    return max_score, mean_score, min_score