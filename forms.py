# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:19:51 2020

@author: Gerald
"""

# forms.py

from wtforms import Form, StringField, SelectField, validators

# Class for the search form
class ExperimentSearchForm(Form):
    """Takes in a Form object and outputs a custom form with choices specific to Experiments"""
    choices = [('Experimental ID', 'Experimental ID'),
               ('Set temperature', 'Set temperature'),
               ('Data Values', 'Data Values')]
    select = SelectField('Search for experimental data:', choices=choices)
    search = StringField('')