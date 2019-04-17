"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__, static_url_path="/")

import marvin_ai.views
