# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:16:19 2020

@author: Gerald
"""

# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Change this if using a different database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EBase.db'
app.secret_key = "bmss2"

db = SQLAlchemy(app)