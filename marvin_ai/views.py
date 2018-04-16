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

names = list()
ans = list()


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
    user_name = request.form["username"]
    if user_name == "":
        user_name = "Admin"
    
    names.append(user_name)
    return render_template(
        "form.html",
        username=user_name
        )


@app.route("/generate_test", methods=['GET', 'POST'])
def generate_test():
    ''' prompt for user to start procedure of test '''
    # get data from the form in form.html
    subject_name = request.form["subjectname"]
    topic_name = request.form["topicname"]
    if subject_name == "":
        subject_name = "Sample"
    if topic_name == "":
        topic_name = "Sample"

    names.append(subject_name)
    names.append(topic_name)

    # file containing data to generate test
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(secure_filename(file.filename))

    # generate word/phrase question
    que_ans_pair = generate_trivia(filename)
    # get one of the generated question and answer at random
    q1, a1 = get_a_question(que_ans_pair)
    
    # generate subjective question
    que_ans_pair2 = generate_subj_question(filename)
    # get one of the generated question and answer at random
    q2, a2 = get_a_question(que_ans_pair2)

    ans.append(a1)
    ans.append(a2)

    return render_template(
        "give_test.html",
        username=names[0],
        testname=names[1],
        topicname=names[2],
        ans1=ans[0],
        question1=q1,
        question2=q2
        )


@ app.route("/output", methods=["GET", "POST"])
def output():
    """ give result based on the test taken by the user """
    # catch user input from the test
    user_ans1 = request.form["answer1"]
    user_ans2 = request.form["answer2"]
    
    obj_score = 0
    subj_score = 0
    total_score = 0
    
    s1 = "Wrong"
    s2 = "Wrong"
    
    # evaluate objective answer
    if user_ans1.upper() == ans[0].upper():
        obj_score = 100
        s1 = "Correct"
    
    # evaluate subjective answer
    if user_ans2 != "":
        subj_score = evaluate_subj_answer(ans[1], user_ans2)
        if subj_score > 50:
            s2 = "Correct"
    
    total_score = (obj_score + subj_score) / 2
    total_score = round(total_score, 2)

    status_flag = back_up_data(names[0], names[1], names[2], total_score)

    ans.clear()
    
    return render_template(
        "output.html",
        show_score=total_score,
        username=names[0],
        subjectname=names[1],
        topicname=names[2],
        st1=s1,
        st2=s2
    )