# MARVIN - AI Examination System

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1e131fc1944e49ac92cb20c7c1a65771)](https://app.codacy.com/manual/nityansuman/marvin?utm_source=github.com&utm_medium=referral&utm_content=nityansuman/marvin&utm_campaign=Badge_Grade_Settings)
![GitHub](https://img.shields.io/github/license/nityansuman/marvin)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/nityansuman/marvin)
![GitHub repo size](https://img.shields.io/github/repo-size/nityansuman/marvin)
![GitHub language count](https://img.shields.io/github/languages/count/nityansuman/marvin)

![GitHub last commit](https://img.shields.io/github/last-commit/nityansuman/marvin)

Conducting examination and answer sheet evaluation are hectic testing tools for assessing
academic achievement, integration of ideas and ability to recall, but are expensive, resource
and time consuming to generate question and evaluate response manually. Manual evaluating
of answer sheet takes up a significant amount of instructors' valuable time and hence is an
expensive process. Also different security concerns regarding paper leakage is one of the other
challenges to conquer. This project aims to build an automated examination system using
machine learning, natural language toolkit (NLTK), python environment, flask framework,
and web technologies to provide an inexpensive alternative to the current examination system.
We implement a model to automatically generate questions with their respective answers and
assess user responses.

![Homepage](https://raw.githubusercontent.com/nityansuman/marvin/master/src/static/images/homepage.png)

## Getting started

Download or clone the project from github

```
$ git clone https://github.com/nityansuman/marvin.git
```

Create a project environment (Anaconda recommended)
```
$ conda create --name envname python
$ conda activate envname
```

Install prerequisites
```
$ pip install -r REQUIREMENTS.txt

$ python

>>> import nltk
>>> nltk.download("all")
>>> exit() # after download is complete, exit python
```

Run project
```
$ cd marvin

$ python runserver.py
```

**Login Board**
![Login Board](https://raw.githubusercontent.com/nityansuman/marvin/master/src/static/images/pic2.jpg)

**Result Board**
![Result Board](https://raw.githubusercontent.com/nityansuman/marvin/master/src/static/images/pic5.png)

## Support

If you like the work I do, show your appreciation by 'FORK', 'STAR' and 'SHARE'.

Open to all types of collaboration. Feel free to raise a PR.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
