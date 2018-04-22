"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from flask import g
from werkzeug import secure_filename
from marvin_ai import app
from marvin_ai.article import Article
from marvin_ai.subjective_question import generate_subj_question
from marvin_ai.cosine_similarity import evaluate_subj_answer
from marvin_ai.util import generate_trivia, get_a_question, back_up_data

import os
import click
import pandas as pd
import numpy as np

gloabl_names_list = list()
global_answer_list = list()
global_test_id = 1


@app.route('/')
@app.route('/home')
def home():
    ''' Renders the home page '''
    return render_template(
        "index.html",
        date=datetime.now().day,
        month=datetime.now().month,
        year=datetime.now().year
        )


@app.route("/form", methods=['GET', 'POST'])
def form():
    ''' prompt for user to start procedure of test '''
    gloabl_names_list.clear()
    user_name = request.form["username"]
    if user_name == "":
        user_name = "Admin"
    
    gloabl_names_list.append(user_name)

    return render_template(
        "form.html",
        username=user_name
        )


@app.route("/generate_test", methods=['GET', 'POST'])
def generate_test():
    ''' prompt for user to start procedure of test '''
    # get data from the form in form.html
    global_answer_list.clear()
    subject_name = request.form["subjectname"]
    if subject_name == "":
        subject_name = "Test Subject"

    gloabl_names_list.append(subject_name)

    global_test_id = request.form["test_id"]

    # file containing data to generate test
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(secure_filename(file.filename))

    if global_test_id == "1":
        # generate word/phrase question
        que_ans_pair = generate_trivia(filename)
        # get one of the generated question and answer at random
        question_list, answer_list = get_a_question(que_ans_pair)
        global_answer_list.append(answer_list)
    else:
        # generate subjective question
        que_ans_pair = generate_subj_question(filename)
        # get one of the generated question and answer at random
        question_list, answer_list = get_a_question(que_ans_pair)
        global_answer_list.append(answer_list)

    return render_template(
        "give_test.html",
        username=gloabl_names_list[0],
        testname=gloabl_names_list[1],
        ans=answer_list,
        que=question_list
        )


@ app.route("/output", methods=["GET", "POST"])
def output():
    """ give result based on the test taken by the user """
    # catch user input from the test
    user_ans = request.form["answer1"]

    total_score = 0

    if global_test_id == "1":
        # evaluate objective answer
        if user_ans.upper() == global_answer_list[0].upper():
            total_score += 100
            #total_score /= 5
    else:
        # evaluate subjective answer
        if user_ans != "":
            subj_score = evaluate_subj_answer(global_answer_list[0], user_ans)
            total_score += subj_score
            #total_score /= 2

    total_score = round(total_score, 2)

    status_flag = back_up_data(gloabl_names_list[0], gloabl_names_list[1], total_score)
    global_answer_list.clear()
    
    return render_template(
        "output.html",
        show_score=total_score,
        username=gloabl_names_list[0],
        subjectname=gloabl_names_list[1]
    )